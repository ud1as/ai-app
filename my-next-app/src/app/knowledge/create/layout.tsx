'use client'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function CreateKnowledgeLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const steps = [
    { id: 1, title: 'Выберите источник данных', path: '/knowledge/create' },
    { id: 2, title: 'Предварительная обработка и очистка', path: '/knowledge/create/preprocessing' },
    { id: 3, title: 'Выполнить и завершить', path: '/knowledge/create/complete' },
  ]

  return (
    <div className="min-h-screen bg-white flex">
      {/* Left Sidebar */}
      <div className="w-64 border-r border-gray-200 p-6">
        <Link 
          href="/knowledge" 
          className="flex items-center text-gray-600 hover:text-gray-900 mb-8"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          <span>Создать базу знаний</span>
        </Link>

        <div className="space-y-4">
          {steps.map((step) => {
            const isActive = pathname === step.path
            const isPast = steps.findIndex(s => s.path === pathname) >= steps.findIndex(s => s.path === step.path)

            return (
              <div key={step.id} className="flex items-center">
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-sm mr-3
                  ${isActive ? 'bg-blue-100 text-blue-600' : 
                    isPast ? 'bg-gray-100 text-gray-600' : 'bg-gray-100 text-gray-400'}`}
                >
                  {step.id}
                </span>
                <span className={`${isActive ? 'text-blue-600 font-medium' : 
                  isPast ? 'text-gray-600' : 'text-gray-400'}`}>
                  {step.title}
                </span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">
        {children}
      </div>
    </div>
  )
}