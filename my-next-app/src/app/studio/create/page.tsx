'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { botApi } from '@/api/endpoints/bots'
import Link from 'next/link'

export default function CreateBotPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    type: 'ЧАТ-БОТ' as const
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
  
    // Use Promise syntax instead of async/await
    botApi.create({
      name: formData.name,
      description: formData.description
    })
    .then(response => {
      console.log('Bot created successfully:', response)
      router.push('/dashboard')
      // Add a small delay before refresh to ensure navigation completes
      setTimeout(() => {
        router.refresh()
      }, 100)
    })
    .catch(err => {
      console.error('Error creating bot:', err)
      setError(err instanceof Error ? err.message : 'Failed to create bot')
    })
    .finally(() => {
      setIsLoading(false)
    })
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  return (
    <div className="max-w-2xl mx-auto p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Create New Bot</h1>
        <Link
          href="/dashboard"
          className="text-gray-600 hover:text-gray-800"
        >
          Cancel
        </Link>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 text-red-600 rounded-lg">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <label 
            htmlFor="type" 
            className="block text-sm font-medium text-gray-700"
          >
            Bot Type
          </label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="ЧАТ-БОТ">Chat Bot</option>
            <option value="АГЕНТ">Agent</option>
            <option value="РАБОЧИЙ ПРОЦЕСС">Workflow</option>
          </select>
        </div>

        <div className="space-y-2">
          <label 
            htmlFor="name" 
            className="block text-sm font-medium text-gray-700"
          >
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter bot name"
          />
        </div>

        <div className="space-y-2">
          <label 
            htmlFor="description" 
            className="block text-sm font-medium text-gray-700"
          >
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Describe what your bot does"
          />
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="submit"
            disabled={isLoading}
            className={`px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
              ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {isLoading ? 'Creating...' : 'Create Bot'}
          </button>
        </div>
      </form>
    </div>
  )
}