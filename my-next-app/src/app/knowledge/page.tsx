'use client'
import { Plus, Search, Link2, Eye } from 'lucide-react'
import Link from 'next/link'

export default function KnowledgePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Secondary Navigation */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex space-x-2">
          <button className="px-4 py-2 bg-blue-50 text-blue-600 font-medium rounded-full text-sm">
            БАЗЫ ЗНАНИЙ
          </button>
          <button className="px-4 py-2 text-gray-600 hover:bg-gray-50 rounded-full text-sm">
            ДОСТУП К API
          </button>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="search"
              placeholder="Поиск"
              className="pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm w-64 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <button className="px-4 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">
            Все теги ▾
          </button>
          <button className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">
            API внешних знаний
          </button>
        </div>
      </div>

      {/* Empty State */}
      <div className="bg-white rounded-lg p-8">
        <div className="max-w-2xl mx-auto text-center">
          <Link2 className="w-8 h-8 text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600 mb-6">
            Импортируйте свои собственные текстовые данные или записывайте данные в режиме реального времени через Webhook для улучшения контекста LLM.
          </p>
          <Link
            href="knowledge/create"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-6"
          >
            <Plus className="w-5 h-5 mr-2" />
            Создать базу знаний
          </Link>
          <div>
            <Link
              href="#"
              className="text-gray-600 hover:text-gray-800 inline-flex items-center"
            >
              Подключение к внешней базе знаний
              <span className="ml-2">→</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Did you know section */}
      <div className="mt-12">
        <h3 className="text-lg font-medium text-blue-600 mb-2">Знаете ли вы?</h3>
        <p className="text-gray-600">
          Базу знаний можно интегрировать в приложение FRONT-AI в{' '}
          <Link href="#" className="text-blue-600 hover:underline">
            качестве контекста
          </Link>
        </p>
      </div>

      {/* Error Notification (if needed) */}
      <div className="fixed bottom-4 left-4 bg-red-50 text-red-600 px-4 py-2 rounded-full flex items-center">
        <div className="w-2 h-2 bg-red-600 rounded-full mr-2" />
        1 error
        <button className="ml-2 text-red-400 hover:text-red-600">×</button>
      </div>
    </div>
  )
}