'use client'

import { useState, useEffect } from 'react'
import Nav from '@/components/Nav'
import { memoryAPI } from '@/lib/api'

interface Memory {
  title: string
  summary: string
  tags: string
  timestamp: number
  contentHash: string
  monadTx: string
}

export default function Memories() {
  const [memories, setMemories] = useState<Memory[]>([])
  const [loading, setLoading] = useState(false)
  const [showAddForm, setShowAddForm] = useState(false)

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
      const stats = await memoryAPI.getStats()

      // For now, we'll show a placeholder
      // In production, you'd call a /list-memories endpoint
      setMemories([])
    } catch (err) {
      console.error('Failed to load memories:', err)
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
      const result = await memoryAPI.insertMemory(content, tags)

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
    if (!query.trim()) return

    try {
      setLoading(true)
      const results = await memoryAPI.searchMemories(query, 10)

      // Convert search results to Memory format
      const formattedMemories = results.map((r: any) => ({
        title: r.text.slice(0, 50) + '...',
        summary: r.text,
        tags: r.tag || '',
        timestamp: Date.now() / 1000,
        contentHash: '',
        monadTx: ''
      }))

      setMemories(formattedMemories)
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
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl md:text-5xl font-black text-kinic-dark mb-3 uppercase tracking-tight">
              <span className="text-gradient">Memories</span>
            </h1>
            <p className="text-lg font-medium text-kinic-text-secondary">
              Browse and manage your stored memories on Kinic
            </p>
          </div>

          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="btn-brutalist px-6 py-3 bg-kinic-orange text-white"
          >
            {showAddForm ? 'Cancel' : '+ Add Memory'}
          </button>
        </div>

        {/* Success/Error Messages */}
        {success && (
          <div className="mb-6 p-4 bg-green-100 border-4 border-black text-green-800 font-bold" style={{ boxShadow: '4px 4px 0 0 #000' }}>
            ✅ {success}
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-red-100 border-4 border-black text-red-800 font-bold" style={{ boxShadow: '4px 4px 0 0 #000' }}>
            ❌ {error}
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

              <div className="flex gap-4">
                <button
                  type="submit"
                  disabled={inserting}
                  className="btn-brutalist px-8 py-3 bg-kinic-cyan text-white disabled:opacity-50"
                >
                  {inserting ? 'Saving to Kinic...' : 'Save Memory'}
                </button>

                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="btn-brutalist px-8 py-3 bg-white text-kinic-dark"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Search Bar */}
        <div className="card mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Search your memories..."
              className="flex-1 bg-white border-4 border-black px-4 py-3 text-kinic-dark font-medium"
              style={{ boxShadow: '4px 4px 0 0 #000' }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSearch(e.currentTarget.value)
                }
              }}
            />
            <button className="btn-brutalist px-6 py-3 bg-kinic-cyan text-white">
              Search
            </button>
          </div>
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
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-black text-kinic-dark uppercase">{memory.title}</h3>
                  <span className="text-xs font-bold text-kinic-text-secondary uppercase">
                    {new Date(memory.timestamp * 1000).toLocaleDateString()}
                  </span>
                </div>

                <p className="text-sm font-medium text-kinic-text-secondary mb-4 line-clamp-3">
                  {memory.summary}
                </p>

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

                {memory.monadTx && (
                  <div className="text-xs font-mono font-bold text-kinic-text-secondary">
                    {memory.monadTx.slice(0, 20)}...
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
