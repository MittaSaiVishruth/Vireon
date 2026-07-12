import fitz  # PyMuPDF
import re
import os
import asyncio
import ollama
import edge_tts
import platform
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image, ImageDraw
from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, afx

class VireonNarrativeEngine:
    def __init__(self, pdf_filename):
        # 1. Absolute Path Resolution
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.pdf_path = os.path.join(self.base_dir, pdf_filename)
        self.output_folder = os.path.join(self.base_dir, "output_assets")
        self.final_folder = os.path.join(self.base_dir, "final_subtopic_videos")
        self.music_file = os.path.join(self.base_dir, "background_music.mp3")
        
        self.segments = []
        self.video_plan = []
        
        for folder in [self.output_folder, self.final_folder]:
            os.makedirs(folder, exist_ok=True)

    # --- PHASE 1: SEMANTIC CLEANING & SEGMENTATION ---
    def process_content(self, threshold=0.55):
        print(f"\n[1/4] Semantic Parsing & Cleaning: {self.pdf_path}")
        if not os.path.exists(self.pdf_path):
            print(f"Error: Could not find {self.pdf_path}")
            return
            
        doc = fitz.open(self.pdf_path)
        text = " ".join([page.get_text().replace("\n", " ") for page in doc])
        
        sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
        sentences = [s.strip() for s in sentence_endings.split(text) if s.strip()]
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)
        
        current_chunk = [sentences[0]]
        for i in range(len(sentences) - 1):
            sim = cosine_similarity(embeddings[i].reshape(1, -1), embeddings[i+1].reshape(1, -1))[0][0]
            if sim < threshold:
                self.segments.append(" ".join(current_chunk))
                current_chunk = [sentences[i+1]]
            else:
                current_chunk.append(sentences[i+1])
        self.segments.append(" ".join(current_chunk))

    # --- PHASE 2: NARRATIVE & ANALOGY DESIGN ---
    def generate_video_plans(self, limit=5):
        print(f"\n[2/4] Designing Analogies and Keywords...")
        for i, content in enumerate(self.segments[:limit]):
            prompt = (
                f"Context: {content[:1200]}\n"
                "Create a high-retention educational segment.\n"
                "1. TITLE: Professional 3-word title.\n"
                "2. KEYWORD: One technical concept (max 2 words).\n"
                "3. SYMBOL: One emoji representing the analogy.\n"
                "4. SCRIPT: A conversational explanation using a simple metaphor (~40 words).\n"
                "Return as: TITLE: [title] | KEYWORD: [keyword] | SYMBOL: [emoji] | SCRIPT: [script]"
            )
            
            try:
                res = ollama.generate(model='llama3', prompt=prompt)['response']
                self.video_plan.append({
                    "index": i + 1,
                    "title": re.search(r"TITLE: (.*?) \|", res).group(1).strip(),
                    "keyword": re.search(r"KEYWORD: (.*?) \|", res).group(1).strip().upper(),
                    "symbol": re.search(r"SYMBOL: (.*?) \|", res).group(1).strip(),
                    "script": re.search(r"SCRIPT: (.*)", res).group(1).strip()
                })
            except Exception:
                self.video_plan.append({"index": i+1, "title":f"Module_{i+1}", "keyword":"CORE", "symbol":"💡", "script":content[:150]})

    # --- PHASE 3: KINETIC UI GENERATION ---
    def draw_visual_context(self, item, progress):
        w, h = 1920, 1080
        img = Image.new('RGB', (w, h), color=(10, 15, 25))
        draw = ImageDraw.Draw(img)

        # Tech Grid
        for x in range(0, w, 120): draw.line([(x, 0), (x, h)], fill=(25, 30, 45), width=1)
        for y in range(0, h, 120): draw.line([(0, y), (w, y)], fill=(25, 30, 45), width=1)
        
        # Sidebar & Progress
        draw.rectangle([0, 0, 480, h], fill=(18, 22, 35))
        draw.rectangle([0, h - int(h * progress), 15, h], fill=(0, 180, 255))

        draw.text((1200, 450), item['symbol'], fill=(255,255,255), anchor="mm", font_size=300)
        draw.text((1200, 780), item['keyword'], fill=(255,255,255), anchor="mm", font_size=100)
        draw.text((80, 120), f"SEGMENT {item['index']}", fill=(120, 140, 200), font_size=40)
        draw.text((80, 180), item['title'].upper(), fill=(255, 255, 255), font_size=55)

        path = os.path.join(self.output_folder, f"frame_{item['index']}.png")
        img.save(path)
        return path

    # --- PHASE 4: KINETIC RENDERING & FIXED AUDIO CLEANUP ---
    async def render_videos(self):
        print(f"\n[3/4] Rendering Kinetic Videos...")
        os.makedirs(self.final_folder, exist_ok=True)
        
        for i, item in enumerate(self.video_plan):
            safe_title = re.sub(r'[\\/*?:"<>|]', '', item['title']).replace(" ", "_")
            video_name = f"{item['index']}_{safe_title}.mp4"
            target_path = os.path.join(self.final_folder, video_name)

            # 1. Voice
            a_path = os.path.join(self.output_folder, f"audio_v_{i}.mp3")
            await edge_tts.Communicate(item['script'], "en-US-AndrewNeural").save(a_path)
            voice = AudioFileClip(a_path)

            # 2. Audio Mix with Music Ducking
            music = None
            if os.path.exists(self.music_file):
                music = AudioFileClip(self.music_file).subclipped(0, voice.duration)
                music = music.with_effects([afx.MultiplyVolume(0.12)])
                final_audio = CompositeAudioClip([voice, music])
            else:
                final_audio = voice

            # 3. Video Assembly
            i_path = self.draw_visual_context(item, (i + 1) / len(self.video_plan))
            clip = ImageClip(i_path).with_duration(voice.duration).with_audio(final_audio)
            clip = clip.resized(lambda t: 1 + 0.08 * (t / voice.duration))
            
            print(f"  > Exporting: {video_name}")
            clip.write_videofile(target_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
            
            # --- CRITICAL FIX: Identity Cleanup ---
            # We use 'is not' to avoid triggering frame comparisons during equality checks
            if final_audio is not voice:
                final_audio.close()
            if music is not None:
                music.close()
            voice.close()
            clip.close()

        print(f"\n[4/4] COMPLETE! Subtopic videos saved to: {self.final_folder}")
        if platform.system() == "Windows":
            os.startfile(self.final_folder)

if __name__ == "__main__":
    PDF_NAME = (r"c:\Users\saivi\OneDrive\Desktop\Work\PDF\The-Complete-Guide-to-Building-Skill-for-Claude.pdf")
    engine = VireonNarrativeEngine(PDF_NAME)
    engine.process_content()
    engine.generate_video_plans(limit=2)
    asyncio.run(engine.render_videos())