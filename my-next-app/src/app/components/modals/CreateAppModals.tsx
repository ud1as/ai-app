'use client'
import { MessageSquare, FileText, Bot, GitBranch } from 'lucide-react'
import { useState } from 'react'

type AppType = 'chatbot' | 'text-generator' | 'agent' | 'workflow'

export default function CreateAppModal({ 
  isOpen, 
  onClose 
}: { 
  isOpen: boolean
  onClose: () => void 
}) {
  const [selectedType, setSelectedType] = useState<AppType>('chatbot')

  if (!isOpen) return null

  const handleClose = (e: React.MouseEvent) => {
    e.stopPropagation()
    onClose()
  }

  return (
    <div className="fixed inset-0 z-50 overflow-auto bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg w-full max-w-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Создать с нуля</h2>
            <button 
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>

          {/* App Type Selection */}
          <div className="mb-6">
            <h3 className="text-base font-medium mb-3">
              Какой тип приложения вы хотите создать?
            </h3>
            <div className="grid grid-cols-4 gap-3">
              {[
                { type: 'chatbot', icon: <MessageSquare className="w-6 h-6 text-blue-500" />, label: 'Чат-бот', bg: 'bg-blue-50' },
                { type: 'text-generator', icon: <FileText className="w-6 h-6 text-green-500" />, label: 'Генератор текста', bg: 'bg-green-50' },
                { type: 'agent', icon: <Bot className="w-6 h-6 text-violet-500" />, label: 'Агент', bg: 'bg-violet-50' },
                { type: 'workflow', icon: <GitBranch className="w-6 h-6 text-orange-500" />, label: 'Рабочий процесс', bg: 'bg-orange-50', beta: true },
              ].map(({ type, icon, label, bg, beta }) => (
                <button
                  key={type}
                  onClick={() => setSelectedType(type as AppType)}
                  className={`p-3 rounded-lg border relative ${
                    selectedType === type 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex flex-col items-center">
                    {icon}
                    <span className="mt-2 text-sm">{label}</span>
                  </div>
                  {beta && (
                    <span className="absolute top-1 right-1 text-[10px] bg-gray-100 px-1.5 py-0.5 rounded">
                      BETA
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          {selectedType === 'chatbot' && (
            <div className="mb-6">
              <h3 className="text-base font-medium mb-3">
                Метод организации чат-бота
              </h3>
              <div className="grid grid-cols-2 gap-3">
                <button className="p-3 rounded-lg border border-blue-500 bg-blue-50 text-left">
                  <div className="font-medium mb-1">Базовый</div>
                  <div className="text-sm text-gray-600">
                    Для начинающих, можно переключиться на Chatflow позже
                  </div>
                </button>
                <button className="p-3 rounded-lg border border-gray-200 text-left relative">
                  <div className="font-medium mb-1">Chatflow</div>
                  <div className="text-sm text-gray-600">
                    Для продвинутых пользователей
                  </div>
                  <span className="absolute top-2 right-2 text-[10px] bg-gray-100 px-1.5 py-0.5 rounded">
                    BETA
                  </span>
                </button>
              </div>
            </div>
          )}

          {/* App Details */}
          <div className="space-y-4">
            <div>
              <h3 className="text-base font-medium mb-3">
                Значок и название приложения
              </h3>
              <div className="flex gap-3">
                <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Bot className="w-5 h-5 text-orange-600" />
                </div>
                <input
                  type="text"
                  placeholder="Дайте вашему приложению имя"
                  className="flex-1 px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <h3 className="text-base font-medium mb-3">Описание</h3>
              <textarea
                placeholder="Введите описание приложения"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg h-24 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Footer */}
          <div className="flex justify-end gap-3 mt-6 pt-4 border-t">
            <button
              onClick={handleClose}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Отмена
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Создать
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}