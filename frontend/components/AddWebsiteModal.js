'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Globe, FileText } from 'lucide-react'
import toast from 'react-hot-toast'
import apiClient from '@/lib/api'

export default function AddWebsiteModal({ onClose, onWebsiteAdded }) {
  const [formData, setFormData] = useState({
    url: '',
    name: '',
    description: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState({})

  // Validation function
  const validateWebsite = (website) => {
    const errors = []
    
    // Check required fields
    if (!website.url || !website.url.trim()) {
      errors.push('Website URL is required')
    }
    
    // Validate URL format
    if (website.url && !website.url.match(/^https?:\/\/.+/)) {
      errors.push('URL must start with http:// or https://')
    }
    
    // Validate name length
    if (website.name && website.name.length > 200) {
      errors.push('Website name must be less than 200 characters')
    }
    
    // Validate description length
    if (website.description && website.description.length > 1000) {
      errors.push('Description must be less than 1000 characters')
    }
    
    return errors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Clear previous errors
    setErrors({})
    
    // Validate form data
    const validationErrors = validateWebsite(formData)
    if (validationErrors.length > 0) {
      // Set field-specific errors
      const fieldErrors = {}
      validationErrors.forEach(error => {
        if (error.includes('URL')) {
          fieldErrors.url = error
        } else if (error.includes('name')) {
          fieldErrors.name = error
        } else if (error.includes('Description')) {
          fieldErrors.description = error
        } else {
          toast.error(error)
        }
      })
      
      setErrors(fieldErrors)
      return
    }
    
    setIsLoading(true)

    try {
      // Sanitize the data
      const sanitizedData = {
        url: formData.url.trim(),
        name: formData.name.trim() || null,
        description: formData.description.trim() || null
      }
      
      const data = await apiClient.createWebsite(sanitizedData)
      toast.success('Website added successfully!')
      onWebsiteAdded(data)
    } catch (error) {
      // Handle specific error types
      if (error.detail) {
        toast.error(error.detail)
      } else if (error.message) {
        toast.error(error.message)
      } else {
        toast.error('Failed to add website')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value
    })
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: null
      })
    }
  }

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.2 }}
          className="bg-white rounded-xl shadow-xl w-full max-w-md"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b">
            <h2 className="text-xl font-semibold text-gray-900">Add New Website</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {/* Website URL */}
            <div>
              <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                Website URL *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Globe className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="url"
                  id="url"
                  name="url"
                  value={formData.url}
                  onChange={handleChange}
                  required
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.url ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
                  }`}
                  placeholder="https://example.com"
                />
              </div>
              {errors.url && (
                <p className="mt-1 text-sm text-red-600">{errors.url}</p>
              )}
              <p className="mt-1 text-sm text-gray-500">
                Enter the full URL of your website (including https://)
              </p>
            </div>

            {/* Website Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Website Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={`block w-full px-3 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.name ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
                }`}
                placeholder="My Awesome Website"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name}</p>
              )}
              <p className="mt-1 text-sm text-gray-500">
                Optional: Give your website a friendly name
              </p>
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 pt-3 pointer-events-none">
                  <FileText className="h-5 w-5 text-gray-400" />
                </div>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={3}
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.description ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
                  }`}
                  placeholder="Brief description of your website..."
                />
              </div>
              {errors.description && (
                <p className="mt-1 text-sm text-red-600">{errors.description}</p>
              )}
              <p className="mt-1 text-sm text-gray-500">
                Optional: Describe what your website is about
              </p>
            </div>

            {/* Buttons */}
            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Adding...' : 'Add Website'}
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </AnimatePresence>
  )
} 