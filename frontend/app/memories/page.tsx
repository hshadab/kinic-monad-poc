'use client'

import { useState, useEffect } from 'react'
import Nav from '@/components/Nav'
import { memoryAPI } from '@/lib/api'
import { useAuth } from '@/lib/useAuth'

interface Memory {
  title: string
  summary: string
  tags: string
  timestamp: number
  contentHash: string
  monadTx: string
  source?: 'kinic' | 'monad'  // Track data source
  fullContent?: string  // Full content from Kinic
  searchScore?: number  // Relevance score from Kinic search
}

export default function Memories() {
  const { principalText, isAuthenticated } = useAuth()
  const [memories, setMemories] = useState<Memory[]>([])
  const [loading, setLoading] = useState(false)
  const [showAddForm, setShowAddForm] = useState(false)
  const [searchMode, setSearchMode] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  // Form state
  const [content, setContent] = useState('')
  const [tags, setTags] = useState('')
  const [inserting, setInserting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  useEffect(() => {
    loadMemories()
  }, [])

  const loadMemories = async () => {
    try {
      setLoading(true)
      setSearchMode(false)
      setSearchQuery('')

      // Fetch memories from Monad blockchain
      const response = await fetch('/list-memories?limit=20')
      if (!response.ok) throw new Error('Failed to fetch memories')

      const data = await response.json()

      // Convert Monad memories to Memory format
      const formattedMemories = data.memories.map((m: any) => ({
        title: m.title,
        summary: m.summary,
        tags: m.tags,
        timestamp: m.timestamp,
        contentHash: m.contentHash,
        monadTx: '',
        source: 'monad' as const,
        fullContent: m.summary  // Monad stores summary, not full content
      }))

      setMemories(formattedMemories)
    } catch (err) {
      console.error('Failed to load memories:', err)
      // If fetch fails, just show empty (might be no memories yet)
      setMemories([])
    } finally {
      setLoading(false)
    }
  }

  const handleInsert = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)

    if (!content.trim()) {
      setError('Content is required')
      return
    }

    try {
      setInserting(true)
      // Pass principal for user isolation
      const result = await memoryAPI.insertMemory(content, tags, principalText || undefined)

      setSuccess(`Memory inserted! Transaction: ${result.monad_tx.slice(0, 16)}...`)
      setContent('')
      setTags('')
      setShowAddForm(false)

      // Refresh memories list
      await loadMemories()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to insert memory')
    } finally {
      setInserting(false)
    }
  }

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      loadMemories()
      return
    }

    try {
      setLoading(true)
      setSearchMode(true)
      setError(null)

      // Pass principal for user isolation
      const results = await memoryAPI.searchMemories(query, 10, principalText || undefined)

      // Convert Kinic search results to Memory format
      const formattedMemories = results.map((r: any) => ({
        title: r.text.slice(0, 60) + (r.text.length > 60 ? '...' : ''),
        summary: r.text.slice(0, 200) + (r.text.length > 200 ? '...' : ''),
        tags: r.tag || '',
        timestamp: Date.now() / 1000,
        contentHash: '',
        monadTx: '',
        source: 'kinic' as const,
        fullContent: r.text,  // Full content from Kinic
        searchScore: r.score  // Relevance score
      }))

      setMemories(formattedMemories)

      if (formattedMemories.length === 0) {
        setError('No results found. Try a different search term.')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary">
      <Nav />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-start gap-4 mb-8">
          <div className="flex-1">
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-kinic-dark mb-3 uppercase tracking-tight">
              <span className="text-gradient">Memories</span>
            </h1>
            <p className="text-base sm:text-lg font-medium text-kinic-text-secondary">
              {isAuthenticated
                ? `Your private memories • ${principalText?.slice(0, 8)}...${principalText?.slice(-4)}`
                : 'Browse and manage your stored memories on Kinic'}
            </p>
          </div>

          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="btn-brutalist px-6 py-3 bg-kinic-orange text-white min-h-[48px] w-full sm:w-auto"
          >
            {showAddForm ? 'Cancel' : '+ Add Memory'}
          </button>
        </div>

        {/* Success/Error Messages */}
        {success && (
          <div className="mb-6 p-4 bg-green-100 border-4 border-black text-green-800 font-bold" style={{ boxShadow: '4px 4px 0 0 #000' }}>
             {success}
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-red-100 border-4 border-black text-red-800 font-bold" style={{ boxShadow: '4px 4px 0 0 #000' }}>
             {error}
          </div>
        )}

        {/* Add Memory Form */}
        {showAddForm && (
          <div className="card mb-8">
            <h2 className="text-2xl font-black text-kinic-dark mb-6 uppercase">Add New Memory</h2>

            <form onSubmit={handleInsert} className="space-y-6">
              <div>
                <label className="block text-sm font-bold text-kinic-dark mb-2 uppercase">
                  Content
                </label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows={6}
                  className="w-full bg-white border-4 border-black px-4 py-3 text-kinic-dark font-medium"
                  style={{ boxShadow: '4px 4px 0 0 #000' }}
                  placeholder="Enter the content you want to remember..."
                  disabled={inserting}
                />
              </div>

              <div>
                <label className="block text-sm font-bold text-kinic-dark mb-2 uppercase">
                  Tags (comma-separated)
                </label>
                <input
                  type="text"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  className="w-full bg-white border-4 border-black px-4 py-3 text-kinic-dark font-medium"
                  style={{ boxShadow: '4px 4px 0 0 #000' }}
                  placeholder="e.g., zkml, machine-learning, research"
                  disabled={inserting}
                />
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  type="submit"
                  disabled={inserting}
                  className="btn-brutalist px-8 py-3 bg-kinic-cyan text-white disabled:opacity-50 min-h-[48px]"
                >
                  {inserting ? 'Saving to Kinic...' : 'Save Memory'}
                </button>

                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="btn-brutalist px-8 py-3 bg-white text-kinic-dark min-h-[48px]"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Search Bar */}
        <div className="card mb-8">
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
            <input
              type="text"
              placeholder="Search your memories with Kinic AI..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 bg-white border-4 border-black px-4 py-3 text-kinic-dark font-medium min-h-[48px]"
              style={{ boxShadow: '4px 4px 0 0 #000' }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSearch(searchQuery)
                }
              }}
            />
            <div className="flex gap-3 sm:gap-4">
              <button
                onClick={() => handleSearch(searchQuery)}
                className="btn-brutalist px-6 py-3 bg-kinic-cyan text-white min-h-[48px] flex-1 sm:flex-none"
              >
                Search
              </button>
              {searchMode && (
                <button
                  onClick={loadMemories}
                  className="btn-brutalist px-6 py-3 bg-white text-kinic-dark min-h-[48px] flex-1 sm:flex-none"
                >
                  Show All
                </button>
              )}
            </div>
          </div>
          {searchMode && (
            <div className="mt-4 text-sm font-bold text-kinic-dark">
              Showing semantic search results from Kinic
            </div>
          )}
        </div>

        {/* Memories List */}
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block w-16 h-16 border-4 border-black" style={{
              borderTopColor: '#23A8E0',
              animation: 'spin 1s linear infinite',
              boxShadow: '4px 4px 0 0 #000'
            }}></div>
            <p className="text-kinic-dark font-bold mt-6 uppercase">Loading memories...</p>
          </div>
        ) : memories.length === 0 ? (
          <div className="card text-center py-12">
            <div className="w-20 h-20 bg-kinic-light border-4 border-black mx-auto mb-6 flex items-center justify-center" style={{ boxShadow: '6px 6px 0 0 #000' }}>
              <svg className="w-10 h-10 text-kinic-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
            </div>
            <h3 className="text-xl font-black text-kinic-dark mb-3 uppercase">No memories yet</h3>
            <p className="text-kinic-text-secondary font-medium mb-6">
              Add your first memory or search to see stored content
            </p>
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-brutalist px-8 py-3 bg-kinic-orange text-white"
            >
              Add Your First Memory
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {memories.map((memory, idx) => (
              <div key={idx} className="card-hover">
                {/* Header with source badge */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-black text-kinic-dark uppercase">{memory.title}</h3>
                  </div>
                  <span className="text-xs font-bold text-kinic-text-secondary uppercase">
                    {new Date(memory.timestamp * 1000).toLocaleDateString()}
                  </span>
                </div>

                {/* Source badge */}
                <div className="flex gap-2 mb-3">
                  <span
                    className={`px-2 py-1 text-xs font-bold uppercase border-2 border-black ${
                      memory.source === 'kinic'
                        ? 'bg-kinic-orange text-white'
                        : 'bg-kinic-purple text-white'
                    }`}
                    style={{ boxShadow: '2px 2px 0 0 #000' }}
                  >
                    {memory.source === 'kinic' ? 'IC/Kinic' : 'Monad Chain'}
                  </span>
                  {memory.searchScore !== undefined && (
                    <span
                      className="px-2 py-1 bg-white text-kinic-dark text-xs font-bold uppercase border-2 border-black"
                      style={{ boxShadow: '2px 2px 0 0 #000' }}
                    >
                      Score: {memory.searchScore.toFixed(2)}
                    </span>
                  )}
                </div>

                {/* Content */}
                <p className="text-sm font-medium text-kinic-text-secondary mb-4 line-clamp-3">
                  {memory.summary}
                </p>

                {/* Tags */}
                {memory.tags && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {memory.tags.split(',').filter(Boolean).map((tag, i) => (
                      <span
                        key={i}
                        className="px-3 py-1 bg-kinic-cyan text-white text-xs font-bold uppercase border-2 border-black"
                        style={{ boxShadow: '2px 2px 0 0 #000' }}
                      >
                        {tag.trim()}
                      </span>
                    ))}
                  </div>
                )}

                {/* Monad metadata */}
                {memory.source === 'monad' && memory.contentHash && (
                  <div className="text-xs font-mono font-bold text-kinic-text-secondary">
                    Hash: {memory.contentHash.slice(0, 20)}...
                  </div>
                )}

                {/* Full content preview for Kinic */}
                {memory.source === 'kinic' && memory.fullContent && memory.fullContent.length > memory.summary.length && (
                  <details className="mt-2">
                    <summary className="text-xs font-bold text-kinic-dark uppercase cursor-pointer">
                      Show Full Content
                    </summary>
                    <p className="text-xs font-medium text-kinic-text-secondary mt-2 p-2 bg-white border-2 border-black">
                      {memory.fullContent}
                    </p>
                  </details>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
