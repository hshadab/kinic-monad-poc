'use client'

import Link from 'next/link'
import Nav from '@/components/Nav'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary">
      <Nav />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="pt-20 pb-16 text-center">
          <h1 className="text-5xl md:text-7xl font-black mb-8 uppercase tracking-tight leading-none">
            <span className="text-kinic-dark block mb-2" style={{ textShadow: '6px 6px 0 #23A8E0' }}>AI Memory</span>
            <span className="text-gradient block" style={{ textShadow: '6px 6px 0 rgba(0,0,0,0.1)' }}>on Monad</span>
          </h1>

          <p className="text-xl md:text-2xl font-bold text-kinic-dark max-w-3xl mx-auto mb-12 leading-tight">
            Store notes, research, and conversations with AI-powered semantic search.
            <span className="block mt-2 text-kinic-cyan">Every operation logged on Monad blockchain.</span>
          </p>

          <div className="flex justify-center gap-6 flex-wrap">
            <Link
              href="/chat"
              className="btn-brutalist px-10 py-5 bg-kinic-orange text-white text-lg"
            >
              Start Chatting
            </Link>
            <Link
              href="/dashboard"
              className="btn-brutalist px-10 py-5 bg-white text-kinic-dark text-lg"
            >
              View Dashboard
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 pb-20">
          <div className="card-hover">
            <div className="w-16 h-16 bg-kinic-cyan border-4 border-black flex items-center justify-center mb-4" style={{ boxShadow: '5px 5px 0 0 #000' }}>
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">AI Chat</h3>
            <p className="text-base font-medium text-kinic-dark leading-snug">
              Claude Haiku AI retrieves relevant memories for intelligent, context-aware responses.
            </p>
          </div>

          <div className="card-hover">
            <div className="w-16 h-16 bg-kinic-pink border-4 border-black flex items-center justify-center mb-4" style={{ boxShadow: '5px 5px 0 0 #000' }}>
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">Semantic Search</h3>
            <p className="text-base font-medium text-kinic-dark leading-snug">
              Search by meaning with vector embeddings via Kinic API on Internet Computer.
            </p>
          </div>

          <div className="card-hover">
            <div className="w-16 h-16 bg-kinic-yellow border-4 border-black flex items-center justify-center mb-4" style={{ boxShadow: '5px 5px 0 0 #000' }}>
              <svg className="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">Blockchain</h3>
            <p className="text-base font-medium text-kinic-dark leading-snug">
              Every operation logged on Monad with human-readable metadata and public audit trail.
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="border-t border-kinic-gray-200 pt-16 pb-20">
          <h2 className="text-3xl font-bold text-center mb-12">
            <span className="text-kinic-dark">Built with </span>
            <span className="text-gradient">Best-in-Class Tech</span>
          </h2>

          <div className="grid md:grid-cols-4 gap-6 text-center">
            <div className="p-6">
              <div className="text-4xl mb-2">🧠</div>
              <h4 className="font-semibold text-kinic-dark mb-1">Claude AI</h4>
              <p className="text-sm text-kinic-text-secondary">Anthropic Haiku</p>
            </div>
            <div className="p-6">
              <div className="text-4xl mb-2">🔍</div>
              <h4 className="font-semibold text-kinic-dark mb-1">Kinic</h4>
              <p className="text-sm text-kinic-text-secondary">Semantic Storage</p>
            </div>
            <div className="p-6">
              <div className="text-4xl mb-2"></div>
              <h4 className="font-semibold text-kinic-dark mb-1">Monad</h4>
              <p className="text-sm text-kinic-text-secondary">High-Speed Blockchain</p>
            </div>
            <div className="p-6">
              <div className="text-4xl mb-2">🌐</div>
              <h4 className="font-semibold text-kinic-dark mb-1">Internet Computer</h4>
              <p className="text-sm text-kinic-text-secondary">Decentralized Compute</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-kinic-gray-200 py-8 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-kinic-text-secondary">
          <p>Built with Kinic, Monad, and Internet Computer</p>
        </div>
      </footer>
    </div>
  )
}
