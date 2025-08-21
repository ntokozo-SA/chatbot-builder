import React from 'react'

const ChatButton = ({ isOpen, onClick, config }) => {
  return (
    <button
      onClick={onClick}
      className={`
        fixed bottom-4 right-4 w-14 h-14 rounded-full shadow-lg 
        transition-all duration-300 ease-in-out transform
        ${isOpen 
          ? 'scale-90 opacity-0 pointer-events-none' 
          : 'scale-100 opacity-100 hover:scale-110'
        }
        flex items-center justify-center
        bg-gradient-to-r from-blue-500 to-blue-600
        hover:from-blue-600 hover:to-blue-700
        text-white
        focus:outline-none focus:ring-4 focus:ring-blue-300
        z-50
      `}
      style={{
        backgroundColor: config.primaryColor,
        boxShadow: `0 4px 12px ${config.primaryColor}40`
      }}
      aria-label="Open chat"
    >
      {isOpen ? (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      ) : (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      )}
    </button>
  )
}

export default ChatButton 