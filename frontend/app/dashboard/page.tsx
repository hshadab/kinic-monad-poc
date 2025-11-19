'use client'

import { useState, useEffect } from 'react'
import Nav from '@/components/Nav'
import StatsCard from '@/components/StatsCard'
import MemoryCard from '@/components/MemoryCard'
import { memoryAPI, monadAPI } from '@/lib/api'
import { useAuth } from '@/lib/useAuth'

interface Stats {
  total_memories_on_chain: number
  agent_memories: number
  contract_address: string
  agent_address: string
}

interface RecentActivity {
  id: number
  title: string
  opType: number
  timestamp: number
  tags: string
}

export default function Dashboard() {
  const { principalText, isAuthenticated } = useAuth()
  const [stats, setStats] = useState<Stats | null>(null)
  const [userMemoryCount, setUserMemoryCount] = useState<number>(0)
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadStats()
  }, [isAuthenticated, principalText])

  const loadStats = async () => {
    try {
      setLoading(true)
      const data = await memoryAPI.getStats()
      setStats(data)

      // If user is authenticated, get their memory count and recent activity
      if (isAuthenticated && principalText) {
        try {
          const userMemories = await monadAPI.search({
            tags: `principal:${principalText}`,
            limit: 100
          })
          setUserMemoryCount(userMemories.num_results)

          // Get recent activity (last 10 operations)
          const recentOps = userMemories.results.slice(0, 10).map((memory: any) => ({
            id: memory.id,
            title: memory.title,
            opType: memory.opType,
            timestamp: memory.timestamp,
            tags: memory.tags
          }))
          setRecentActivity(recentOps)
        } catch (err) {
          console.error('Failed to load user stats:', err)
        }
      } else {
        // If not authenticated, show global recent activity
        try {
          const recentMemories = await monadAPI.getRecent(10)
          const recentOps = recentMemories.map((memory: any) => ({
            id: memory.id,
            title: memory.title,
            opType: memory.opType,
            timestamp: memory.timestamp,
            tags: memory.tags
          }))
          setRecentActivity(recentOps)
        } catch (err) {
          console.error('Failed to load recent activity:', err)
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load stats')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary">
      <Nav />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-kinic-dark mb-3 uppercase tracking-tight">
            <span className="text-gradient">Dashboard</span>
          </h1>
          <p className="text-base sm:text-lg font-medium text-kinic-text-secondary">
            {isAuthenticated
              ? `Your personal dashboard • ${principalText?.slice(0, 8)}...${principalText?.slice(-4)}`
              : 'Monitor your memory operations and blockchain activity'}
          </p>
        </div>

        {loading ? (
          <div className="text-center py-20">
            <div className="inline-block w-16 h-16 border-4 border-black" style={{
              borderTopColor: '#23A8E0',
              animation: 'spin 1s linear infinite',
              boxShadow: '4px 4px 0 0 #000'
            }}></div>
            <p className="text-kinic-dark font-bold mt-6 uppercase">Loading dashboard...</p>
          </div>
        ) : error ? (
          <div className="text-center py-20">
            <div className="w-20 h-20 bg-red-100 border-4 border-black mx-auto mb-6 flex items-center justify-center" style={{ boxShadow: '6px 6px 0 0 #000' }}>
              <svg className="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-red-600 font-bold text-lg mb-4">{error}</p>
            <button
              onClick={loadStats}
              className="btn-brutalist px-6 py-3 bg-kinic-orange text-white"
            >
              Retry
            </button>
          </div>
        ) : (
          <>
            {/* Stats Grid */}
            <div className="grid md:grid-cols-4 gap-6 mb-12">
              {isAuthenticated && (
                <StatsCard
                  title="Your Memories"
                  value={userMemoryCount}
                  icon={
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  }
                />
              )}

              <StatsCard
                title={isAuthenticated ? "Global Memories" : "Total Memories"}
                value={stats?.total_memories_on_chain || 0}
                icon={
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                }
              />

              <StatsCard
                title="Agent Memories"
                value={stats?.agent_memories || 0}
                icon={
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                }
              />

              <StatsCard
                title="Blockchain Logs"
                value={stats?.total_memories_on_chain || 0}
                icon={
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                }
              />

              <StatsCard
                title="Network Status"
                value="Live"
                icon={
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                }
              />
            </div>

            {/* Contract Info */}
            <div className="grid md:grid-cols-2 gap-6 mb-12">
              <div className="card">
                <h3 className="text-xl font-black text-kinic-dark mb-4 uppercase">Smart Contract</h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">Contract Address</p>
                    <p className="text-sm font-mono font-bold text-kinic-cyan break-all">
                      {stats?.contract_address || 'Not deployed'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">Network</p>
                    <p className="text-sm font-bold text-kinic-dark">Monad Private Mainnet (Chain ID: 143)</p>
                  </div>
                  <a
                    href={`https://mainnet-beta.monvision.io/address/${stats?.contract_address}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-sm font-bold text-kinic-cyan hover:text-kinic-cyan-light uppercase"
                  >
                    View on Explorer
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
              </div>

              <div className="card">
                <h3 className="text-xl font-black text-kinic-dark mb-4 uppercase">Agent Info</h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">Agent Address</p>
                    <p className="text-sm font-mono font-bold text-kinic-cyan break-all">
                      {stats?.agent_address || 'Not configured'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">AI Model</p>
                    <p className="text-sm font-bold text-kinic-dark">Claude Haiku (Anthropic)</p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">Storage</p>
                    <p className="text-sm font-bold text-kinic-dark">Internet Computer (Kinic)</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="card">
              <h3 className="text-xl font-black text-kinic-dark mb-4 uppercase">
                {isAuthenticated ? 'Your Recent Activity' : 'Global Recent Activity'}
              </h3>

              {recentActivity.length === 0 ? (
                <p className="text-kinic-text-secondary font-medium text-center py-8">
                  No recent activity. Start by <a href="/chat" className="text-kinic-cyan font-bold hover:text-kinic-cyan-light uppercase">chatting with the AI</a>
                </p>
              ) : (
                <div className="space-y-3">
                  {recentActivity.map((activity) => (
                    <div key={activity.id} className="flex items-start justify-between p-4 bg-kinic-light border-3 border-black hover:shadow-md transition-all" style={{ boxShadow: '3px 3px 0 0 #000' }}>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2">
                          <span
                            className={`px-2 py-1 text-xs font-bold uppercase border-2 border-black ${
                              activity.opType === 0
                                ? 'bg-kinic-cyan text-white'
                                : activity.opType === 1
                                ? 'bg-kinic-purple text-white'
                                : 'bg-kinic-orange text-white'
                            }`}
                            style={{ boxShadow: '2px 2px 0 0 #000' }}
                          >
                            {activity.opType === 0 ? 'INSERT' : activity.opType === 1 ? 'SEARCH' : 'CHAT'}
                          </span>
                          <span className="text-xs font-bold text-kinic-text-secondary uppercase">
                            {new Date(activity.timestamp * 1000).toLocaleString()}
                          </span>
                        </div>
                        <p className="text-sm font-bold text-kinic-dark line-clamp-1 mb-2">
                          {activity.title}
                        </p>
                        {activity.tags && (
                          <div className="flex flex-wrap gap-1">
                            {activity.tags.split(',').filter(Boolean).slice(0, 3).map((tag, i) => (
                              <span
                                key={i}
                                className="px-2 py-1 bg-white text-kinic-dark text-xs font-bold border-2 border-black"
                                style={{ boxShadow: '1px 1px 0 0 #000' }}
                              >
                                {tag.trim()}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </main>
    </div>
  )
}
