'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Zap, Settings, Sun, PiggyBank } from 'lucide-react'

export default function PreprocessingPage() {
  const router = useRouter()
  const [method, setMethod] = useState('automatic')
  const [quality, setQuality] = useState('high')

  return (
    <div>
      <div className="flex items-center mb-8">
        <Link href="/knowledge/create" className="text-gray-600 hover:text-gray-900">
          ← Создать базу знаний
        </Link>
      </div>

      <h1 className="text-2xl font-semibold mb-8">
        Предварительная обработка и очистка текста
      </h1>

      <div className="space-y-8 max-w-3xl">
        <div>
          <h2 className="text-lg font-medium mb-4">Настройки фрагментации</h2>
          <div className="space-y-4">
            <div
              className={`p-4 border rounded-lg cursor-pointer ${
                method === 'automatic' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
              }`}
              onClick={() => setMethod('automatic')}
            >
              <div className="flex items-start">
                <Zap className="w-6 h-6 text-blue-600 mr-3 mt-1" />
                <div>
                  <h3 className="font-medium mb-1">Автоматически</h3>
                  <p className="text-gray-600">
                    Автоматически устанавливать правила фрагментации и предварительной обработки.
                    Пользователям, не знакомым с системой, рекомендуется выбрать этот вариант.
                  </p>
                </div>
              </div>
            </div>

            <div
              className={`p-4 border rounded-lg cursor-pointer ${
                method === 'custom' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
              }`}
              onClick={() => setMethod('custom')}
            >
              <div className="flex items-start">
                <Settings className="w-6 h-6 text-gray-600 mr-3 mt-1" />
                <div>
                  <h3 className="font-medium mb-1">Пользовательский</h3>
                  <p className="text-gray-600">
                    Настроить правила фрагментации, длину фрагментов, правила предварительной 
                    обработки и т. д.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-lg font-medium mb-4">Режим индексации</h2>
          <div className="grid grid-cols-2 gap-4">
            <div
              className={`p-4 border rounded-lg cursor-pointer ${
                quality === 'high' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
              }`}
              onClick={() => setQuality('high')}
            >
              <Sun className="w-6 h-6 text-yellow-500 mb-2" />
              <h3 className="font-medium">Высокое качество</h3>
              <span className="text-blue-600 text-sm">Рекомендуется</span>
            </div>

            <div
              className={`p-4 border rounded-lg cursor-pointer ${
                quality === 'economic' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
              }`}
              onClick={() => setQuality('economic')}
            >
              <PiggyBank className="w-6 h-6 text-blue-600 mb-2" />
              <h3 className="font-medium">Экономичный</h3>
            </div>
          </div>
        </div>

        <div className="pt-8 flex justify-between">
          <Link
            href="/knowledge/create"
            className="px-4 py-2 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50"
          >
            Предыдущий шаг
          </Link>
          <button
            onClick={() => router.push('/knowledge/create/complete')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Сохранить и обработать
          </button>
        </div>
      </div>
    </div>
  )
}