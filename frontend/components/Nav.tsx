'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Nav() {
  const pathname = usePathname()

  const links = [
    { href: '/', label: 'Home' },
    { href: '/memories', label: 'Memories' },
    { href: '/discover', label: 'Discover' },
    { href: '/chat', label: 'Chat' },
    { href: '/dashboard', label: 'Dashboard' },
  ]

  return (
    <nav className="border-b-4 border-black bg-white sticky top-0 z-50" style={{ boxShadow: '0 4px 0 0 #000' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3">
            <img
              src="https://cdn.prod.website-files.com/6712749157ea3bf4a781f309/671bbee00d9198b08a63cb40_kinic-logo.svg"
              alt="Kinic Logo"
              className="h-10 w-auto"
            />
            <span className="text-2xl font-black text-kinic-dark uppercase tracking-tight">
              AI <span className="text-gradient">MEMORY AGENT</span>
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex space-x-2">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-5 py-2 font-bold uppercase text-sm transition-all duration-100 border-3 border-black ${
                  pathname === link.href
                    ? 'bg-kinic-cyan text-white'
                    : 'bg-white text-kinic-dark hover:bg-kinic-yellow'
                }`}
                style={{
                  boxShadow: pathname === link.href ? '3px 3px 0 0 #000' : '2px 2px 0 0 #000'
                }}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Connection Status */}
          <div className="flex items-center space-x-2 px-3 py-1 border-3 border-black bg-green-400" style={{ boxShadow: '3px 3px 0 0 #000' }}>
            <div className="w-3 h-3 bg-black"></div>
            <span className="text-sm font-bold text-black uppercase">Live</span>
          </div>
        </div>
      </div>
    </nav>
  )
}
