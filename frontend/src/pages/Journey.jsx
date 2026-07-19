import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { CheckCircle2, Circle, Loader2, Sparkles, BookOpen, Brain, PenTool, Video, Check } from 'lucide-react'
import { motion } from 'framer-motion'

const STAGES = [
  { id: 'upload', label: 'Upload Document', icon: BookOpen, completedEvent: 'upload_complete' },
  { id: 'document', label: 'Document Analysis', icon: Brain, completedEvent: 'document_processed' },
  { id: 'curriculum', label: 'Curriculum Planning', icon: BookOpen, completedEvent: 'curriculum_generated' },
  { id: 'lesson', label: 'Lesson Generation', icon: PenTool, completedEvent: 'lesson_generated' },
  { id: 'storyboard', label: 'Storyboard Creation', icon: Sparkles, completedEvent: 'storyboard_generated' },
  { id: 'assessment', label: 'Quiz Generation', icon: CheckCircle2, completedEvent: 'assessment_generated' },
  { id: 'video', label: 'Educational Rendering', icon: Video, completedEvent: 'video_generated' },
]

export default function Journey() {
  const { courseId } = useParams()
  const navigate = useNavigate()
  const [completedStages, setCompletedStages] = useState(['upload'])
  const [activeStage, setActiveStage] = useState('document')
  const [error, setError] = useState(null)

  useEffect(() => {
    // Connect to SSE
    const eventSource = new EventSource(`http://localhost:8000/api/stream/${courseId}`)

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      const type = data.event_type
      
      console.log("Received event:", type)

      if (type === 'agent_failed') {
        setError(data.payload.error || 'An error occurred during generation.')
        eventSource.close()
        return
      }

      // Map backend events to stages
      const stageMap = {
        'document_processed': 'curriculum',
        'curriculum_generated': 'lesson',
        'lesson_generated': 'storyboard', // concurrent with assessment
        'assessment_generated': 'video', 
        'storyboard_generated': 'video',
        'video_generated': 'done'
      }

      setCompletedStages(prev => {
        // Find which stage this event completes
        const stageObj = STAGES.find(s => s.completedEvent === type)
        if (stageObj && !prev.includes(stageObj.id)) {
          return [...prev, stageObj.id]
        }
        return prev
      })

      if (stageMap[type]) {
        setActiveStage(stageMap[type])
      }

      if (type === 'video_generated') {
        // We are done! Redirect to workspace after a small delay to show completion
        setTimeout(() => {
          navigate(`/workspace/${courseId}`)
        }, 2000)
      }
    }

    eventSource.onerror = (err) => {
      console.error("SSE Error:", err)
      // Usually means connection lost, but we'll let it try to reconnect natively
    }

    return () => {
      eventSource.close()
    }
  }, [courseId, navigate])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 max-w-4xl mx-auto">
      
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-16"
      >
        <div className="flex items-center justify-center gap-3 mb-4">
          <Sparkles className="w-8 h-8 text-primary animate-pulse" />
          <h1 className="text-3xl font-bold tracking-tight">AI Generation Journey</h1>
        </div>
        <p className="text-lg text-foreground/60 max-w-xl mx-auto">
          Our AI agents are working together to transform your document into a complete learning experience.
        </p>
      </motion.div>

      {error ? (
        <div className="w-full max-w-xl p-6 bg-red-500/10 border border-red-500/20 rounded-2xl text-center">
          <p className="text-red-400 font-semibold mb-2">Generation Failed</p>
          <p className="text-sm text-red-400/80">{error}</p>
          <button 
            onClick={() => navigate('/')}
            className="mt-6 px-6 py-2 bg-card hover:bg-card-hover rounded-full text-sm font-medium transition-colors"
          >
            Go Back
          </button>
        </div>
      ) : (
        <div className="w-full max-w-2xl bg-card border border-border rounded-3xl p-8 md:p-12 shadow-2xl relative overflow-hidden">
          {/* Animated Background Blob */}
          <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-primary/10 rounded-full blur-3xl opacity-50 animate-pulse" />
          <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl opacity-50 animate-pulse" />

          <div className="relative z-10 space-y-8">
            {STAGES.map((stage, index) => {
              const isCompleted = completedStages.includes(stage.id)
              const isActive = activeStage === stage.id && !isCompleted
              const isPending = !isCompleted && !isActive
              const Icon = stage.icon

              return (
                <div key={stage.id} className="flex items-center gap-6">
                  <div className="relative">
                    {/* Connecting line */}
                    {index !== STAGES.length - 1 && (
                      <div className={`absolute top-10 left-1/2 -ml-[1px] w-[2px] h-12 transition-colors duration-500 ${isCompleted ? 'bg-primary' : 'bg-border'}`} />
                    )}
                    
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-500 ${
                      isCompleted ? 'bg-primary text-white shadow-lg shadow-primary/30 scale-100' :
                      isActive ? 'bg-primary/20 text-primary ring-2 ring-primary ring-offset-2 ring-offset-card scale-110' :
                      'bg-card-hover text-foreground/30 scale-100'
                    }`}>
                      {isCompleted ? <Check className="w-5 h-5" /> : <Icon className="w-5 h-5" />}
                    </div>
                  </div>
                  
                  <div className="flex-1 flex items-center justify-between">
                    <div>
                      <h3 className={`text-lg font-medium transition-colors duration-300 ${
                        isCompleted || isActive ? 'text-foreground' : 'text-foreground/40'
                      }`}>
                        {stage.label}
                      </h3>
                      {isActive && (
                        <p className="text-sm text-primary animate-pulse mt-1">AI agent is working...</p>
                      )}
                    </div>
                    {isActive && (
                      <Loader2 className="w-5 h-5 text-primary animate-spin" />
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
