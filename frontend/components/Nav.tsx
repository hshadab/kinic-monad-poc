'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LoginButton } from './LoginButton'

export default function Nav() {
  const pathname = usePathname()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const links = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/memories', label: 'Memories' },
    { href: '/discover', label: 'Discover' },
    { href: '/chat', label: 'Chat' },
    { href: '/dashboard', label: 'Dashboard' },
  ]

  return (
    <nav className="border-b-4 border-black bg-white sticky top-0 z-50" style={{ boxShadow: '0 4px 0 0 #000' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo - Responsive sizing */}
          <Link href="/" className="flex items-center space-x-2 flex-shrink-0">
            <img
              src="https://cdn.prod.website-files.com/6712749157ea3bf4a781f309/671bbee00d9198b08a63cb40_kinic-logo.svg"
              alt="Kinic Logo"
              className="h-8 sm:h-10 w-auto"
            />
            <span className="text-lg sm:text-2xl font-black text-kinic-dark uppercase tracking-tight hidden xs:inline">
              AI <span className="text-gradient">MEMORY</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex space-x-2">
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

          {/* Right Side: Desktop */}
          <div className="hidden md:flex items-center space-x-2 sm:space-x-3">
            {/* Connection Status - Hide on small screens */}
            <div className="hidden sm:flex items-center space-x-2 px-2 sm:px-3 py-1 border-3 border-black bg-green-400" style={{ boxShadow: '3px 3px 0 0 #000' }}>
              <div className="w-3 h-3 bg-black"></div>
              <span className="text-xs sm:text-sm font-bold text-black uppercase">Live</span>
            </div>

            {/* Internet Identity Login */}
            <LoginButton />
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden px-3 py-2 border-3 border-black bg-kinic-cyan text-white"
            style={{ boxShadow: '3px 3px 0 0 #000' }}
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {mobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={3}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={3}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden border-t-4 border-black py-4 space-y-2">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`block px-4 py-3 font-bold uppercase text-sm transition-all duration-100 border-3 border-black ${
                  pathname === link.href
                    ? 'bg-kinic-cyan text-white'
                    : 'bg-white text-kinic-dark active:bg-kinic-yellow'
                }`}
                style={{
                  boxShadow: pathname === link.href ? '3px 3px 0 0 #000' : '2px 2px 0 0 #000'
                }}
              >
                {link.label}
              </Link>
            ))}

            {/* Mobile Login */}
            <div className="md:hidden pt-2">
              <LoginButton />
            </div>

            {/* Mobile Connection Status */}
            <div className="sm:hidden flex items-center justify-center space-x-2 px-3 py-2 border-3 border-black bg-green-400" style={{ boxShadow: '3px 3px 0 0 #000' }}>
              <div className="w-3 h-3 bg-black"></div>
              <span className="text-sm font-bold text-black uppercase">Live</span>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
