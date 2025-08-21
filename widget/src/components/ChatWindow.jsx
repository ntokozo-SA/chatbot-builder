import React, { useState } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'

const ChatWindow = ({ 
  isOpen, 
  messages, 
  isLoading, 
  onSendMessage, 
  onClose, 
  config,
  messagesEndRef 
}) => {
  const [inputValue, setInputValue] = useState('')

  const handleSendMessage = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue)
      setInputValue('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed bottom-20 right-4 w-96 h-[500px] bg-white rounded-lg shadow-xl border border-gray-200 flex flex-col z-50 animate-bounce-in">
      {/* Header */}
      <div 
        className="flex items-center justify-between p-4 border-b border-gray-200 rounded-t-lg"
        style={{ backgroundColor: config.primaryColor }}
      >
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h3 className="text-white font-semibold text-lg">{config.title}</h3>
            <p className="text-white text-opacity-80 text-sm">{config.subtitle}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-white hover:text-opacity-80 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList 
          messages={messages} 
          isLoading={isLoading}
          messagesEndRef={messagesEndRef}
        />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <MessageInput
          value={inputValue}
          onChange={setInputValue}
          onSend={handleSendMessage}
          onKeyPress={handleKeyPress}
          isLoading={isLoading}
          placeholder="Type your message..."
        />
      </div>
    </div>
  )
}

export default ChatWindow 