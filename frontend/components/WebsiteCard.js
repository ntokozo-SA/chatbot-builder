'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Globe, 
  Settings, 
  Trash2, 
  Play, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  MessageSquare,
  Copy,
  ExternalLink,
  Bot
} from 'lucide-react'
import toast from 'react-hot-toast'
import apiClient from '@/lib/api'
import ChatbotDemo from './ChatbotDemo'

export default function WebsiteCard({ website, onDelete, onUpdate, index }) {
  const [isLoading, setIsLoading] = useState(false)
  const [showWidgetCode, setShowWidgetCode] = useState(false)
  const [showChatbotDemo, setShowChatbotDemo] = useState(false)

  const getStatusIcon = () => {
    switch (website.status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-600" />
      case 'scraping':
      case 'processing':
        return <Clock className="w-5 h-5 text-yellow-600" />
      default:
        return <Clock className="w-5 h-5 text-gray-400" />
    }
  }

  const getStatusColor = () => {
    switch (website.status) {
      case 'completed':
        return 'text-green-600 bg-green-100'
      case 'failed':
        return 'text-red-600 bg-red-100'
      case 'scraping':
      case 'processing':
        return 'text-yellow-600 bg-yellow-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusText = () => {
    switch (website.status) {
      case 'completed':
        return 'Ready'
      case 'failed':
        return 'Failed'
      case 'scraping':
        return 'Scraping'
      case 'processing':
        return 'Processing'
      default:
        return 'Pending'
    }
  }

  const handleStartScraping = async () => {
    setIsLoading(true)
    try {
      await apiClient.startScraping(website.id)
      toast.success('Website scraping started!')
      // Update the website status
      onUpdate({ ...website, status: 'scraping' })
    } catch (error) {
      toast.error(error.message || 'Failed to start scraping')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this website? This action cannot be undone.')) {
      return
    }

    setIsLoading(true)
    try {
      await apiClient.deleteWebsite(website.id)
      toast.success('Website deleted successfully')
      onDelete(website.id)
    } catch (error) {
      toast.error(error.message || 'Failed to delete website')
    } finally {
      setIsLoading(false)
    }
  }

  const copyWidgetCode = () => {
    const widgetCode = `<script src="${process.env.NEXT_PUBLIC_BACKEND_URL}/widget.js" data-website-id="${website.id}"></script>`
    navigator.clipboard.writeText(widgetCode)
    toast.success('Widget code copied to clipboard!')
  }

  const widgetCode = `<script src="${process.env.NEXT_PUBLIC_BACKEND_URL}/widget.js" data-website-id="${website.id}"></script>`

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
    >
      {/* Header */}
      <div className="p-6 border-b">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Globe className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                {website.name || 'Untitled Website'}
              </h3>
              <p className="text-sm text-gray-500 truncate max-w-xs">
                {website.url}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor()}`}>
              {getStatusText()}
            </span>
            {getStatusIcon()}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {website.description && (
          <p className="text-gray-600 text-sm mb-4">
            {website.description}
          </p>
        )}

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{website.pages_scraped || 0}</p>
            <p className="text-xs text-gray-500">Pages Scraped</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{website.total_chunks || 0}</p>
            <p className="text-xs text-gray-500">Content Chunks</p>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          {website.status === 'pending' && (
            <button
              onClick={handleStartScraping}
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              <Play className="w-4 h-4" />
              <span>Start Scraping</span>
            </button>
          )}

          {website.status === 'completed' && (
            <>
              <button
                onClick={() => setShowChatbotDemo(true)}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2"
              >
                <Bot className="w-4 h-4" />
                <span>View Chatbot</span>
              </button>
              
              <button
                onClick={() => setShowWidgetCode(!showWidgetCode)}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
              >
                <MessageSquare className="w-4 h-4" />
                <span>Get Widget Code</span>
              </button>
              
              {showWidgetCode && (
                <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Widget Code:</span>
                    <button
                      onClick={copyWidgetCode}
                      className="text-blue-600 hover:text-blue-700 text-sm flex items-center space-x-1"
                    >
                      <Copy className="w-3 h-3" />
                      <span>Copy</span>
                    </button>
                  </div>
                  <code className="text-xs bg-white p-2 rounded border block overflow-x-auto">
                    {widgetCode}
                  </code>
                </div>
              )}
            </>
          )}

          <div className="flex space-x-2">
            <button
              onClick={() => window.open(website.url, '_blank')}
              className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center space-x-2"
            >
              <ExternalLink className="w-4 h-4" />
              <span>Visit</span>
            </button>
            <button
              onClick={handleDelete}
              disabled={isLoading}
              className="flex-1 border border-red-300 text-red-600 py-2 px-4 rounded-lg hover:bg-red-50 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              <Trash2 className="w-4 h-4" />
              <span>Delete</span>
            </button>
          </div>
        </div>
      </div>
      
      {/* Chatbot Demo Modal */}
      <ChatbotDemo
        website={website}
        isOpen={showChatbotDemo}
        onClose={() => setShowChatbotDemo(false)}
      />
    </motion.div>
  )
} 