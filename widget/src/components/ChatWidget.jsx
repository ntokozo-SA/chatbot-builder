import React, { useState, useRef, useEffect } from 'react'
import ChatButton from './ChatButton'
import ChatWindow from './ChatWindow'

const ChatWidget = ({ websiteId, config }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState([])
  const [conversationId, setConversationId] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (message) => {
    if (!message.trim()) return

    const userMessage = {
      id: Date.now(),
      content: message,
      role: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch(`${config.backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          website_id: websiteId,
          conversation_id: conversationId
        })
      })

      const data = await response.json()

      if (response.ok) {
        const botMessage = {
          id: Date.now() + 1,
          content: data.message,
          role: 'assistant',
          timestamp: new Date(),
          sources: data.sources
        }

        setMessages(prev => [...prev, botMessage])
        setConversationId(data.conversation_id)
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          content: 'Sorry, I encountered an error. Please try again.',
          role: 'assistant',
          timestamp: new Date(),
          isError: true
        }
        setMessages(prev => [...prev, errorMessage])
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        content: 'Sorry, I\'m having trouble connecting. Please check your internet connection and try again.',
        role: 'assistant',
        timestamp: new Date(),
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleToggle = () => {
    setIsOpen(!isOpen)
  }

  return (
    <div className="ai-chatbot-widget">
      <ChatWindow
        isOpen={isOpen}
        messages={messages}
        isLoading={isLoading}
        onSendMessage={sendMessage}
        onClose={() => setIsOpen(false)}
        config={config}
        messagesEndRef={messagesEndRef}
      />
      <ChatButton
        isOpen={isOpen}
        onClick={handleToggle}
        config={config}
      />
    </div>
  )
}

export default ChatWidget 