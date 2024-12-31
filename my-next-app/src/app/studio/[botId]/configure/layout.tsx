'use client'
import { Settings, History } from 'lucide-react'
import Link from 'next/link'
import { useParams, usePathname } from 'next/navigation'

export default function BotsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const params = useParams()
  const botId = params.id

  return (
    <div>
      {/* Top Navigation */}
      <div className="border-b border-gray-200">
        <div className="max-w-[1400px] mx-auto">
          <div className="flex">
            <Link
              href={`/studio/bots/${botId}/config`}
              className={`flex items-center px-6 py-3 ${
                pathname.includes('/config')
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Settings className="w-4 h-4 mr-2" />
              Настройки
            </Link>
            <Link
              href={`/studio/bots/${botId}/logs`}
              className={`flex items-center px-6 py-3 ${
                pathname.includes('/logs')
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <History className="w-4 h-4 mr-2" />
              Логи
            </Link>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-[1400px] mx-auto">
        {children}
      </div>
    </div>
  )
}