import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, Loader2, BookOpen } from 'lucide-react'
import { motion } from 'framer-motion'

export default function Home() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true)
    } else if (e.type === 'dragleave') {
      setIsDragging(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile)
        setError(null)
      } else {
        setError('Please upload a valid PDF document.')
      }
    }
  }, [])

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const handleGenerate = async () => {
    if (!file) return

    setIsUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to upload file')
      }

      const data = await response.json()
      
      if (data.course_id) {
        navigate(`/journey/${data.course_id}`)
      }
    } catch (err) {
      setError(err.message)
      setIsUploading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <div className="flex items-center justify-center gap-3 mb-6">
          <div className="bg-primary/20 p-3 rounded-2xl ring-1 ring-primary/50">
            <BookOpen className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight">Vireon</h1>
        </div>
        <h2 className="text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary to-purple-400">
          Turn Documents into Learning.
        </h2>
        <p className="text-xl text-foreground/70 max-w-2xl mx-auto">
          Upload any PDF and watch our AI instantly generate a complete, interactive course with lessons, videos, and quizzes.
        </p>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="w-full max-w-xl"
      >
        <div 
          className={`relative overflow-hidden group flex flex-col items-center justify-center w-full h-80 p-8 border-2 border-dashed rounded-3xl transition-all duration-300 ease-in-out cursor-pointer ${
            isDragging ? 'border-primary bg-primary/10' : 'border-border bg-card hover:border-primary/50 hover:bg-card-hover'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-upload').click()}
        >
          {/* Animated Background Gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          
          <input
            id="file-upload"
            type="file"
            className="hidden"
            accept="application/pdf"
            onChange={handleFileChange}
          />
          
          {!file ? (
            <div className="flex flex-col items-center z-10">
              <div className="p-4 bg-background rounded-full mb-4 group-hover:scale-110 transition-transform duration-300 shadow-xl ring-1 ring-border">
                <Upload className="w-8 h-8 text-primary" />
              </div>
              <p className="mb-2 text-lg font-medium">
                <span className="text-primary">Click to upload</span> or drag and drop
              </p>
              <p className="text-sm text-foreground/50">PDF files up to 100 pages</p>
            </div>
          ) : (
            <div className="flex flex-col items-center z-10 w-full">
              <div className="p-4 bg-primary/20 rounded-full mb-4 ring-1 ring-primary/50">
                <FileText className="w-10 h-10 text-primary" />
              </div>
              <p className="mb-4 text-lg font-medium text-center truncate w-full px-8">
                {file.name}
              </p>
              <p className="text-sm text-foreground/50 mb-6">
                {(file.size / (1024 * 1024)).toFixed(2)} MB
              </p>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleGenerate()
                }}
                disabled={isUploading}
                className="w-full max-w-xs py-3 px-6 rounded-full bg-primary hover:bg-primary-hover text-white font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-primary/25"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Generating Course...
                  </>
                ) : (
                  'Generate Course ✨'
                )}
              </button>
            </div>
          )}
        </div>
        
        {error && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-center text-sm"
          >
            {error}
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}
