'use client'
import { Settings } from 'lucide-react'
import Link from 'next/link'

export default function BotLogsPage() {
  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Top Navigation */}
      <div className="mb-8">
        <div className="flex border-b border-gray-200">
          <Link
            href="../config"
            className="flex items-center px-6 py-3 text-gray-600 hover:text-gray-900"
          >
            <Settings className="w-4 h-4 mr-2" />
            Настройки
          </Link>
          <Link
            href="."
            className="flex items-center px-6 py-3 border-b-2 border-blue-600 text-blue-600"
          >
            Логи
          </Link>
        </div>
      </div>

      {/* Logs Content */}
      <div>
        <h2 className="text-lg mb-4">История логов</h2>
        {/* Add your logs content here */}
      </div>
    </div>
  )
}