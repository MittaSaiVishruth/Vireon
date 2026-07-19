import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Loader2, PlayCircle, FileText, CheckSquare, Layers, Download, ChevronRight, Menu, X, BrainCircuit } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Workspace() {
  const { courseId } = useParams()
  const navigate = useNavigate()
  
  const [course, setCourse] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  const [activeModuleId, setActiveModuleId] = useState(null)
  const [activeLessonId, setActiveLessonId] = useState(null)
  const [activeTab, setActiveTab] = useState('notes') // 'notes', 'flashcards', 'quiz'
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/courses/${courseId}`)
        if (!response.ok) throw new Error('Failed to fetch course details')
        const data = await response.json()
        setCourse(data)
        
        // Set initial selection
        if (data.modules && data.modules.length > 0) {
          const firstMod = data.modules[0]
          setActiveModuleId(firstMod.module_id)
          if (firstMod.lessons && firstMod.lessons.length > 0) {
            setActiveLessonId(firstMod.lessons[0].lesson_id)
          }
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    
    fetchCourse()
  }, [courseId])

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <Loader2 className="w-10 h-10 text-primary animate-spin" />
      </div>
    )
  }

  if (error || !course) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="text-center p-8 bg-card rounded-3xl border border-border">
          <p className="text-red-400 mb-4">{error || "Course not found"}</p>
          <button onClick={() => navigate('/')} className="px-6 py-2 bg-primary rounded-full">Go Home</button>
        </div>
      </div>
    )
  }

  // Get active lesson data
  let activeLesson = null
  if (activeModuleId && activeLessonId) {
    const mod = course.modules.find(m => m.module_id === activeModuleId)
    if (mod) {
      activeLesson = mod.lessons.find(l => l.lesson_id === activeLessonId)
    }
  }

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      
      {/* Mobile Sidebar Toggle */}
      <button 
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-card border border-border rounded-lg"
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
      >
        {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Sidebar Navigation */}
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="w-72 flex-shrink-0 bg-card border-r border-border h-full flex flex-col absolute md:relative z-40"
          >
            <div className="p-6 border-b border-border">
              <div className="flex items-center gap-2 mb-2">
                <BrainCircuit className="w-6 h-6 text-primary" />
                <h1 className="font-bold text-lg truncate" title={course.title}>Vireon Course</h1>
              </div>
              <p className="text-sm text-foreground/50 truncate">{course.title}</p>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
              {course.modules.map(module => (
                <div key={module.module_id}>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-foreground/40 mb-3 px-2">
                    {module.title}
                  </h3>
                  <div className="space-y-1">
                    {module.lessons.map(lesson => (
                      <button
                        key={lesson.lesson_id}
                        onClick={() => {
                          setActiveModuleId(module.module_id)
                          setActiveLessonId(lesson.lesson_id)
                          if (window.innerWidth < 768) setIsSidebarOpen(false)
                        }}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-all ${
                          activeLessonId === lesson.lesson_id 
                            ? 'bg-primary/10 text-primary font-medium' 
                            : 'hover:bg-card-hover text-foreground/70 hover:text-foreground'
                        }`}
                      >
                        <PlayCircle className={`w-4 h-4 flex-shrink-0 ${activeLessonId === lesson.lesson_id ? 'text-primary' : 'text-foreground/40'}`} />
                        <span className="text-sm truncate">{lesson.title}</span>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="p-4 border-t border-border">
              <button 
                onClick={() => { /* Export logic to be implemented on backend */ }}
                className="w-full flex items-center justify-center gap-2 py-2.5 bg-card-hover hover:bg-border rounded-xl text-sm transition-colors"
              >
                <Download className="w-4 h-4" />
                Export Course Notes
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        {activeLesson ? (
          <>
            {/* Video Player Header Section */}
            <div className="flex-shrink-0 bg-black/40 border-b border-border aspect-video max-h-[45vh] w-full relative flex items-center justify-center overflow-hidden">
              {activeLesson.video_path ? (
                <video 
                  controls 
                  className="w-full h-full object-contain"
                  src={`http://localhost:8000/api/videos/${activeLesson.video_path}`}
                  poster="/poster-placeholder.png"
                />
              ) : (
                <div className="text-center text-foreground/50 p-8">
                  <PlayCircle className="w-16 h-16 mx-auto mb-4 opacity-20" />
                  <p>Video is still rendering or unavailable.</p>
                </div>
              )}
            </div>

            {/* Content Tabs Header */}
            <div className="flex items-center border-b border-border bg-card/50 backdrop-blur-md px-6">
              <div className="flex gap-1 overflow-x-auto no-scrollbar">
                {[
                  { id: 'notes', label: 'Lesson Notes', icon: FileText },
                  { id: 'flashcards', label: 'Flashcards', icon: Layers },
                  { id: 'quiz', label: 'Quiz', icon: CheckSquare }
                ].map(tab => {
                  const Icon = tab.icon
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center gap-2 px-5 py-4 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
                        activeTab === tab.id 
                          ? 'border-primary text-primary' 
                          : 'border-transparent text-foreground/50 hover:text-foreground hover:bg-card-hover'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {tab.label}
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Scrollable Content Body */}
            <div className="flex-1 overflow-y-auto p-6 md:p-10">
              <div className="max-w-4xl mx-auto">
                {activeTab === 'notes' && (
                  <div className="prose prose-invert prose-p:text-foreground/80 max-w-none">
                    <h2 className="text-3xl font-bold mb-4">{activeLesson.title}</h2>
                    <p className="text-lg text-foreground/60 mb-8">{activeLesson.description}</p>
                    
                    {/* Render actual content logic if present in activeLesson.content */}
                    {activeLesson.content ? (
                       <div>
                         {activeLesson.content.sections?.map((sec, i) => (
                           <div key={i} className="mb-8">
                             <h3 className="text-xl font-semibold mb-3">{sec.heading}</h3>
                             <p className="whitespace-pre-wrap">{sec.text}</p>
                           </div>
                         ))}
                       </div>
                    ) : (
                      <p className="text-foreground/40 italic">No notes generated for this lesson.</p>
                    )}
                  </div>
                )}
                
                {activeTab === 'flashcards' && (
                  <div className="grid gap-6 md:grid-cols-2">
                    {activeLesson.assessment?.flashcards?.map((fc, i) => (
                      <div key={i} className="group perspective-1000">
                        <div className="relative w-full h-48 transition-transform duration-500 transform-style-preserve-3d group-hover:rotate-y-180">
                          {/* Front */}
                          <div className="absolute w-full h-full bg-card border border-border rounded-2xl p-6 flex flex-col justify-center items-center text-center backface-hidden shadow-lg">
                            <span className="text-xs uppercase text-primary font-bold tracking-widest mb-2">Question</span>
                            <p className="text-lg font-medium">{fc.question}</p>
                          </div>
                          {/* Back */}
                          <div className="absolute w-full h-full bg-primary/10 border border-primary/30 rounded-2xl p-6 flex flex-col justify-center items-center text-center backface-hidden rotate-y-180 shadow-lg">
                            <span className="text-xs uppercase text-primary font-bold tracking-widest mb-2">Answer</span>
                            <p className="text-lg font-medium">{fc.answer}</p>
                          </div>
                        </div>
                      </div>
                    )) || <p className="text-foreground/40 italic col-span-2">No flashcards available.</p>}
                  </div>
                )}
                
                {activeTab === 'quiz' && (
                  <div className="space-y-8">
                    {activeLesson.assessment?.quiz?.map((q, i) => (
                      <div key={i} className="bg-card border border-border rounded-2xl p-6 shadow-sm">
                        <h3 className="font-medium text-lg mb-4">
                          <span className="text-primary mr-2">Q{i + 1}.</span> {q.question}
                        </h3>
                        <div className="space-y-2">
                          {q.options?.map((opt, j) => (
                            <label key={j} className="flex items-center p-3 rounded-xl hover:bg-card-hover border border-transparent hover:border-border cursor-pointer transition-all">
                              <input type="radio" name={`quiz-${i}`} className="text-primary focus:ring-primary mr-3 w-4 h-4" />
                              <span className="text-foreground/80">{opt}</span>
                            </label>
                          ))}
                        </div>
                      </div>
                    )) || <p className="text-foreground/40 italic">No quiz available.</p>}
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="flex h-full items-center justify-center text-foreground/40">
            Select a lesson to begin learning.
          </div>
        )}
      </div>
    </div>
  )
}
