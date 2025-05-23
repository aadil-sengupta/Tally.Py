import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'
import { BrowserRouter } from 'react-router-dom'


// createRoot(document.getElement8yId('root')).render(
//   <StrictMode> 
//     <div className="flex flex-col items-center justify-center h-screen">
//       <h1 className="text-4xl font-bold">TallyAI</h1>
//       <p className="mt-4 text-lg">Your AI-powered assistant for all your needs.</p>
//     </div>    
//   </StrictMode>,
// )

const container = document.getElementById('root')
const root = createRoot(container)
root.render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)