// src/app/studio/page.tsx
'use client'
import { useState } from 'react'
import { FileText, Plus, History } from 'lucide-react'
import Link from 'next/link'

interface Bot {
  id: string;
  name: string;
  type: 'ЧАТ-БОТ' | 'АГЕНТ' | 'РАБОЧИЙ ПРОЦЕСС';
  description?: string;
  icon?: string;
}

export default function StudioPage() {
  const [bots] = useState<Bot[]>([
    { 
      id: '1', 
      name: 'sdvs', 
      type: 'ЧАТ-БОТ' 
    },
    // ... other bots
  ])

  return (
    <div className="p-8">
      {/* Create Application Section */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          СОЗДАТЬ ПРИЛОЖЕНИЕ
        </h2>
        <div className="space-y-3">
          <Link 
            href="/studio/create"
            className="w-full flex items-center text-left px-4 py-3 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
          >
            <Plus className="w-5 h-5 mr-3" />
            <span>Создать с нуля</span>
          </Link>
          {/* ... other buttons */}
        </div>
      </div>

      {/* Bots Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {bots.map((bot) => (
          <Link
            key={bot.id}
            href={`/studio/bots/${bot.id}/config`} // Updated path
            className="block p-6 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
          >
            <div className="flex items-start">
              <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center mr-3">
                {bot.icon || '🤖'}
              </div>
              <div>
                <h3 className="font-medium mb-1">{bot.name}</h3>
                <div className="text-xs text-gray-500 mb-2">{bot.type}</div>
                {bot.description && (
                  <p className="text-sm text-gray-600 line-clamp-2">
                    {bot.description}
                  </p>
                )}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}