'use client'
import { Search } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { label: 'Все', href: '/studio' },
  { label: 'Чат-бот', href: '/studio/chatbot' },
  { label: 'Агент', href: '/studio/agent' },
  { label: 'Рабочий процесс', href: '/studio/workflow' }
]

export default function StudioHeader() {
  const pathname = usePathname()

  return (
    <div className="flex flex-col space-y-6 mb-8">
      {/* Navigation */}
      <div className="flex items-center justify-between">
        <div className="flex space-x-2">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-4 py-2 rounded-full text-sm ${
                pathname === item.href
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
        
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="search"
              placeholder="Поиск"
              className="pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm w-64 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="px-4 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">
            Все теги ▾
          </button>
        </div>
      </div>
    </div>
  )
}