'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { MonitorPlay, BookOpen, Star, Search, Wrench } from 'lucide-react'

type NavLinkProps = {
  href: string
  children: React.ReactNode
  icon: React.ReactNode
  isHighlighted?: boolean
}

const NavLink = ({ href, children, icon, isHighlighted }: NavLinkProps) => {
  const pathname = usePathname()
  const isActive = pathname.startsWith(href)

  return (
    <Link
      href={href}
      className={`${
        isActive || isHighlighted
          ? 'bg-blue-50 text-blue-600'
          : 'text-gray-600 hover:bg-gray-50'
      } flex items-center px-4 py-2 rounded-lg transition-colors`}
    >
      {icon}
      <span className="ml-2">{children}</span>
    </Link>
  )
}

export default function Navbar() {
  const pathname = usePathname()

  // Hide navbar on specific paths
  const excludedPaths = ['/login', '/register']
  if (excludedPaths.includes(pathname)) {
    return null
  }

  return (
    <nav className="border-b border-gray-200 bg-white font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Left section */}
          <div className="flex items-center gap-4">
            <Link href="/" className="text-2xl font-bold text-blue-600 mr-4">
              FLITCHAT
            </Link>
          </div>
          
          {/* Center section - Main Navigation */}
          <div className="flex items-center space-x-2">
            <NavLink href="/explore" icon={<Search className="w-5 h-5" />}>
              Исследовать
            </NavLink>
            <NavLink href="/studio" icon={<MonitorPlay className="w-5 h-5" />}>
              Студия
            </NavLink>
            <NavLink href="/knowledge" icon={<BookOpen className="w-5 h-5" />}>
              Знания
            </NavLink>
            <NavLink href="/tools" icon={<Wrench className="w-5 h-5" />}>
              Инструменты
            </NavLink>
          </div>

          {/* Right section - User */}
          <div className="flex items-center">
            <button className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white">
              D
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
