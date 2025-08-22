'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { 
  Bot, 
  Plus, 
  Globe, 
  Settings, 
  LogOut, 
  User, 
  MessageSquare, 
  Activity,
  ExternalLink,
  Copy,
  CheckCircle,
  AlertCircle,
  Clock,
  Play
} from 'lucide-react'
import toast from 'react-hot-toast'
import AddWebsiteModal from '../../components/AddWebsiteModal'
import WebsiteCard from '../../components/WebsiteCard'
import apiClient from '@/lib/api'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [websites, setWebsites] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [stats, setStats] = useState({
    totalWebsites: 0,
    activeChatbots: 0,
    totalConversations: 0,
    totalMessages: 0
  })

  useEffect(() => {
    checkAuth()
    fetchUserData()
    fetchWebsites()
  }, [])

  const checkAuth = () => {
    const token = localStorage.getItem('authToken')
    if (!token) {
      router.push('/login')
    }
  }

  const fetchUserData = () => {
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
  }

  const fetchWebsites = async () => {
    try {
      const data = await apiClient.getWebsites()
      setWebsites(data)
      setStats({
        totalWebsites: data.length,
        activeChatbots: data.filter(w => w.status === 'completed').length,
        totalConversations: data.reduce((sum, w) => sum + (w.total_conversations || 0), 0),
        totalMessages: data.reduce((sum, w) => sum + (w.total_messages || 0), 0)
      })
    } catch (error) {
      toast.error(error.message || 'Failed to fetch websites')
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    router.push('/')
  }

  const handleWebsiteAdded = (newWebsite) => {
    setWebsites([newWebsite, ...websites])
    setStats(prev => ({
      ...prev,
      totalWebsites: prev.totalWebsites + 1
    }))
    setShowAddModal(false)
  }

  const handleWebsiteDeleted = (websiteId) => {
    setWebsites(websites.filter(w => w.id !== websiteId))
    setStats(prev => ({
      ...prev,
      totalWebsites: prev.totalWebsites - 1
    }))
  }

  const handleWebsiteUpdated = (updatedWebsite) => {
    setWebsites(websites.map(w => w.id === updatedWebsite.id ? updatedWebsite : w))
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Bot className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">AI Chatbot Builder</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{user?.full_name || user?.email}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.full_name?.split(' ')[0] || 'there'}!
          </h1>
          <p className="text-gray-600">
            Manage your AI chatbots and monitor their performance.
          </p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Globe className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Websites</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalWebsites}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Bot className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Chatbots</p>
                <p className="text-2xl font-bold text-gray-900">{stats.activeChatbots}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <MessageSquare className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Conversations</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalConversations}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Activity className="w-6 h-6 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Messages</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalMessages}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Websites Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Websites</h2>
            <button
              onClick={() => setShowAddModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Add Website</span>
            </button>
          </div>

          {websites.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <Globe className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No websites yet</h3>
              <p className="text-gray-600 mb-6">
                Add your first website to start building an AI chatbot.
              </p>
              <button
                onClick={() => setShowAddModal(true)}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add Your First Website
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {websites.map((website, index) => (
                <WebsiteCard
                  key={website.id}
                  website={website}
                  onDelete={handleWebsiteDeleted}
                  onUpdate={handleWebsiteUpdated}
                  index={index}
                />
              ))}
            </div>
          )}
        </motion.div>
      </div>

      {/* Add Website Modal */}
      {showAddModal && (
        <AddWebsiteModal
          onClose={() => setShowAddModal(false)}
          onWebsiteAdded={handleWebsiteAdded}
        />
      )}
    </div>
  )
} 