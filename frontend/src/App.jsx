import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Journey from './pages/Journey'
import Workspace from './pages/Workspace'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-foreground selection:bg-primary/30">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/journey/:courseId" element={<Journey />} />
          <Route path="/workspace/:courseId" element={<Workspace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
