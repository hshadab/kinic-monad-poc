'use client'

import { useState, useEffect } from 'react'
import Nav from '@/components/Nav'
import { monadAPI, MonadMemory, TrendingTag, MonadStatsResponse } from '@/lib/api'
import AuthGuard from '@/components/AuthGuard'

export default function Discover() {
  const [memories, setMemories] = useState<MonadMemory[]>([])
  const [trending, setTrending] = useState<TrendingTag[]>([])
  const [stats, setStats] = useState<MonadStatsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState<'tags' | 'title' | 'recent'>('tags')
  const [filterOpType, setFilterOpType] = useState<number | undefined>(undefined)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    setLoading(true)
    try {
      // Load trending tags and recent memories in parallel
      const [trendingData, recentData, statsData] = await Promise.all([
        monadAPI.getTrending(15),
        monadAPI.getRecent(20),
        monadAPI.getStats()
      ])

      setTrending(trendingData)
      setMemories(recentData)
      setStats(statsData)
    } catch (err) {
      console.error('Failed to load discover data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim() && searchType !== 'recent') {
      return
    }

    setLoading(true)
    try {
      let results: MonadMemory[] = []

      if (searchType === 'tags') {
        results = await monadAPI.searchByTags(searchQuery, 50)
      } else if (searchType === 'title') {
        const response = await monadAPI.search({
          title: searchQuery,
          limit: 50,
          op_type: filterOpType
        })
        results = response.results
      } else {
        results = await monadAPI.getRecent(50)
      }

      setMemories(results)
    } catch (err) {
      console.error('Search failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleTagClick = async (tag: string) => {
    setSearchQuery(tag)
    setSearchType('tags')
    setLoading(true)
    try {
      const results = await monadAPI.searchByTags(tag, 50)
      setMemories(results)
    } catch (err) {
      console.error('Tag search failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = async () => {
    setLoading(true)
    try {
      await monadAPI.refresh()
      await loadInitialData()
    } catch (err) {
      console.error('Refresh failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary">
        <Nav />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-kinic-dark uppercase tracking-tight">
              <span className="text-gradient">Discover</span>
            </h1>
            <button
              onClick={handleRefresh}
              className="btn-brutalist px-4 py-3 bg-kinic-purple text-white text-sm min-h-[48px]"
              disabled={loading}
            >
              🔄 Refresh Cache
            </button>
          </div>
          <p className="text-lg font-medium text-kinic-text-secondary mb-4">
            Explore on-chain memories from Monad blockchain
          </p>

          {/* Stats Bar */}
          {stats && stats.synced && (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              <div className="card-compact bg-white">
                <div className="text-xs font-bold text-kinic-text-secondary uppercase mb-1">Total</div>
                <div className="text-2xl font-black text-kinic-dark">{stats.total_memories}</div>
              </div>
              <div className="card-compact bg-kinic-cyan text-white">
                <div className="text-xs font-bold uppercase mb-1">Inserts</div>
                <div className="text-2xl font-black">{stats.insert_operations}</div>
              </div>
              <div className="card-compact bg-kinic-purple text-white">
                <div className="text-xs font-bold uppercase mb-1">Searches</div>
                <div className="text-2xl font-black">{stats.search_operations}</div>
              </div>
              <div className="card-compact bg-kinic-orange text-white">
                <div className="text-xs font-bold uppercase mb-1">Unique Tags</div>
                <div className="text-2xl font-black">{stats.unique_tags}</div>
              </div>
              <div className="card-compact bg-kinic-yellow text-kinic-dark">
                <div className="text-xs font-bold uppercase mb-1">Users</div>
                <div className="text-2xl font-black">{stats.unique_users}</div>
              </div>
            </div>
          )}
        </div>

        {/* Search Section */}
        <div className="card mb-8">
          <h2 className="text-2xl font-black text-kinic-dark mb-4 uppercase">Search Monad Metadata</h2>

          {/* Search Type Selector */}
          <div className="flex flex-wrap gap-2 mb-4">
            <button
              onClick={() => setSearchType('tags')}
              className={`px-4 py-3 md:py-2 font-bold uppercase text-sm border-3 border-black ${
                searchType === 'tags'
                  ? 'bg-kinic-cyan text-white'
                  : 'bg-white text-kinic-dark'
              }`}
              style={{ boxShadow: '3px 3px 0 0 #000' }}
            >
              By Tags
            </button>
            <button
              onClick={() => setSearchType('title')}
              className={`px-4 py-3 md:py-2 font-bold uppercase text-sm border-3 border-black ${
                searchType === 'title'
                  ? 'bg-kinic-cyan text-white'
                  : 'bg-white text-kinic-dark'
              }`}
              style={{ boxShadow: '3px 3px 0 0 #000' }}
            >
              By Title
            </button>
            <button
              onClick={() => { setSearchType('recent'); handleSearch(); }}
              className={`px-4 py-3 md:py-2 font-bold uppercase text-sm border-3 border-black ${
                searchType === 'recent'
                  ? 'bg-kinic-cyan text-white'
                  : 'bg-white text-kinic-dark'
              }`}
              style={{ boxShadow: '3px 3px 0 0 #000' }}
            >
              Recent
            </button>
          </div>

          {/* Search Input */}
          {searchType !== 'recent' && (
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="text"
                placeholder={
                  searchType === 'tags'
                    ? 'Enter tags (comma-separated)...'
                    : 'Enter title keywords...'
                }
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 bg-white border-4 border-black px-4 py-3 text-kinic-dark font-medium min-h-[48px]"
                style={{ boxShadow: '4px 4px 0 0 #000' }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch()
                  }
                }}
              />
              <button
                onClick={handleSearch}
                className="btn-brutalist px-6 py-3 bg-kinic-orange text-white min-h-[48px]"
                disabled={loading}
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          )}

          {/* Operation Type Filter */}
          <div className="flex flex-wrap gap-3 mt-4">
            <span className="text-sm font-bold text-kinic-dark uppercase w-full sm:w-auto">Filter:</span>
            <label className="flex items-center gap-2 cursor-pointer min-h-[44px]">
              <input
                type="radio"
                name="opType"
                checked={filterOpType === undefined}
                onChange={() => setFilterOpType(undefined)}
                className="w-5 h-5"
              />
              <span className="text-sm font-bold text-kinic-dark uppercase">All</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer min-h-[44px]">
              <input
                type="radio"
                name="opType"
                checked={filterOpType === 0}
                onChange={() => setFilterOpType(0)}
                className="w-5 h-5"
              />
              <span className="text-sm font-bold text-kinic-dark uppercase">Inserts Only</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer min-h-[44px]">
              <input
                type="radio"
                name="opType"
                checked={filterOpType === 1}
                onChange={() => setFilterOpType(1)}
                className="w-5 h-5"
              />
              <span className="text-sm font-bold text-kinic-dark uppercase">Searches Only</span>
            </label>
          </div>
        </div>

        {/* Trending Tags */}
        <div className="card mb-8">
          <h2 className="text-2xl font-black text-kinic-dark mb-4 uppercase">
            🔥 Trending Topics
          </h2>
          <div className="flex flex-wrap gap-2">
            {trending.map((tag, idx) => (
              <button
                key={idx}
                onClick={() => handleTagClick(tag.tag)}
                className="px-4 py-2 bg-kinic-yellow text-kinic-dark font-bold uppercase text-sm border-3 border-black hover:bg-kinic-orange hover:text-white transition-colors"
                style={{ boxShadow: '3px 3px 0 0 #000' }}
              >
                {tag.tag} ({tag.count})
              </button>
            ))}
          </div>
        </div>

        {/* Results */}
        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block w-16 h-16 border-4 border-black" style={{
              borderTopColor: '#23A8E0',
              animation: 'spin 1s linear infinite',
              boxShadow: '4px 4px 0 0 #000'
            }}></div>
            <p className="text-kinic-dark font-bold mt-6 uppercase">Searching blockchain...</p>
          </div>
        ) : memories.length === 0 ? (
          <div className="card text-center py-12">
            <h3 className="text-xl font-black text-kinic-dark mb-3 uppercase">No results found</h3>
            <p className="text-kinic-text-secondary font-medium">
              Try different search terms or explore trending topics above
            </p>
          </div>
        ) : (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-black text-kinic-dark uppercase">
                Results ({memories.length})
              </h2>
              <span className="text-sm font-bold text-kinic-text-secondary uppercase">
                Source: Monad Blockchain
              </span>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {memories.map((memory) => (
                <div key={memory.id} className="card-hover">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-lg font-black text-kinic-dark uppercase flex-1">
                      {memory.title}
                    </h3>
                    <span
                      className={`px-2 py-1 text-xs font-bold uppercase border-2 border-black ${
                        memory.opType === 0
                          ? 'bg-kinic-cyan text-white'
                          : 'bg-kinic-purple text-white'
                      }`}
                      style={{ boxShadow: '2px 2px 0 0 #000' }}
                    >
                      {memory.opType === 0 ? 'INSERT' : 'SEARCH'}
                    </span>
                  </div>

                  {/* Summary */}
                  <p className="text-sm font-medium text-kinic-text-secondary mb-4">
                    {memory.summary}
                  </p>

                  {/* Tags */}
                  {memory.tags && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {memory.tags.split(',').filter(Boolean).slice(0, 4).map((tag, i) => (
                        <button
                          key={i}
                          onClick={() => handleTagClick(tag.trim())}
                          className="px-3 py-1 bg-kinic-orange text-white text-xs font-bold uppercase border-2 border-black hover:bg-kinic-yellow hover:text-kinic-dark"
                          style={{ boxShadow: '2px 2px 0 0 #000' }}
                        >
                          {tag.trim()}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Metadata */}
                  <div className="flex justify-between items-center text-xs font-bold text-kinic-text-secondary">
                    <span className="uppercase">
                      {new Date(memory.timestamp * 1000).toLocaleDateString()}
                    </span>
                    <span className="font-mono">
                      ID: {memory.id}
                    </span>
                  </div>

                  {/* Content Hash */}
                  <div className="mt-2 text-xs font-mono font-bold text-kinic-text-secondary break-all">
                    Hash: {memory.contentHash.slice(0, 20)}...
                  </div>

                  {/* User */}
                  <div className="mt-1 text-xs font-mono font-bold text-kinic-text-secondary break-all">
                    User: {memory.user.slice(0, 10)}...
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
    </AuthGuard>
  )
}
