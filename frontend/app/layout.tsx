import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Kinic Memory Agent on Monad',
  description: 'AI-powered memory agent with Kinic storage and Monad blockchain transparency',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
