import React from 'react'
import { createRoot } from 'react-dom/client'
import ChatWidget from './components/ChatWidget'
import './index.css'

// Widget configuration
const defaultConfig = {
  title: 'AI Assistant',
  subtitle: 'Ask me anything about this website',
  primaryColor: '#3b82f6',
  position: 'bottom-right',
  backendUrl: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
}

// Initialize widget
function initWidget(config = {}) {
  const widgetConfig = { ...defaultConfig, ...config }
  
  // Create widget container
  const widgetContainer = document.createElement('div')
  widgetContainer.id = 'ai-chatbot-widget'
  widgetContainer.style.cssText = `
    position: fixed;
    z-index: 999999;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  `
  
  // Position the widget
  if (widgetConfig.position === 'bottom-left') {
    widgetContainer.style.bottom = '20px'
    widgetContainer.style.left = '20px'
  } else if (widgetConfig.position === 'bottom-center') {
    widgetContainer.style.bottom = '20px'
    widgetContainer.style.left = '50%'
    widgetContainer.style.transform = 'translateX(-50%)'
  } else {
    // bottom-right (default)
    widgetContainer.style.bottom = '20px'
    widgetContainer.style.right = '20px'
  }
  
  // Add to page
  document.body.appendChild(widgetContainer)
  
  // Get website ID from script tag
  const scriptTag = document.currentScript || document.querySelector('script[data-website-id]')
  const websiteId = scriptTag?.getAttribute('data-website-id')
  
  if (!websiteId) {
    console.error('AI Chatbot Widget: website-id is required')
    return
  }
  
  // Render widget
  const root = createRoot(widgetContainer)
  root.render(
    <ChatWidget 
      websiteId={websiteId}
      config={widgetConfig}
    />
  )
  
  return {
    destroy: () => {
      root.unmount()
      if (widgetContainer.parentNode) {
        widgetContainer.parentNode.removeChild(widgetContainer)
      }
    }
  }
}

// Auto-initialize if script has data-website-id
if (document.currentScript?.getAttribute('data-website-id')) {
  initWidget()
}

// Export for manual initialization
window.AIChatbotWidget = {
  init: initWidget
} 