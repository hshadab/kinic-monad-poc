'use client'

import { useState } from 'react'
import Nav from '@/components/Nav'
import Chat from '@/components/Chat'
import { chatAPI } from '@/lib/api'
import { useAuth } from '@/lib/useAuth'

interface Message {
  role: 'user' | 'assistant'
  content: string
  memories?: Array<{ text: string; score: number; tag: string }>
  monad_tx?: string
}

export default function ChatPage() {
  const { principalText, isAuthenticated } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Pass principal for user-scoped memory search
      const response = await chatAPI.send({
        message: input,
        top_k: 3,
        principal: principalText || undefined
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        memories: response.memories_used,
        monad_tx: response.monad_tx,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to get response'}`,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary">
      <Nav />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-kinic-dark mb-3 uppercase tracking-tight">
            Chat with AI <span className="text-gradient">Memory Agent</span>
          </h1>
          <p className="text-base sm:text-lg font-medium text-kinic-text-secondary">
            {isAuthenticated
              ? `Ask questions and I'll search your private memories • ${principalText?.slice(0, 8)}...${principalText?.slice(-4)}`
              : 'Ask questions and the AI will search your memories for relevant context'}
          </p>
        </div>

        {/* Chat Messages */}
        <div className="mb-8 min-h-[500px]">
          {messages.length === 0 ? (
            <div className="text-center py-20">
              <div className="w-20 h-20 bg-gradient-monad border-4 border-black mx-auto mb-6 flex items-center justify-center" style={{ boxShadow: '6px 6px 0 0 #000' }}>
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">Start a conversation</h3>
              <p className="text-base font-medium text-kinic-text-secondary max-w-md mx-auto">
                Ask me anything! I'll search your memories and provide context-aware responses.
              </p>

              <div className="mt-8 grid gap-4 max-w-2xl mx-auto">
                <button
                  onClick={() => setInput('What is ZKML?')}
                  className="card-hover text-left p-4"
                >
                  <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">Example question:</p>
                  <p className="text-kinic-dark font-bold">What is ZKML?</p>
                </button>
                <button
                  onClick={() => setInput('Tell me about blockchain performance')}
                  className="card-hover text-left p-4"
                >
                  <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase">Example question:</p>
                  <p className="text-kinic-dark font-bold">Tell me about blockchain performance</p>
                </button>
              </div>
            </div>
          ) : (
            <Chat messages={messages} />
          )}

          {loading && (
            <div className="flex justify-start mt-6">
              <div className="bg-white border-4 border-black p-5" style={{ boxShadow: '6px 6px 0 0 #000' }}>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-kinic-cyan animate-bounce"></div>
                  <div className="w-3 h-3 bg-kinic-pink animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-3 h-3 bg-kinic-orange animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  <span className="text-sm font-bold text-kinic-dark ml-2 uppercase">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Form */}
        <div className="sticky bottom-0 bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary pt-4 pb-8">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={loading}
              className="w-full bg-white border-4 border-black px-4 sm:px-6 py-4 pr-14 sm:pr-16 text-kinic-dark placeholder-kinic-text-secondary font-medium focus:outline-none disabled:opacity-50 min-h-[56px]"
              style={{ boxShadow: '6px 6px 0 0 #000' }}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-3 sm:p-4 bg-gradient-monad border-3 border-black disabled:opacity-50 disabled:cursor-not-allowed hover:transform hover:-translate-y-1 transition-all duration-100 min-w-[48px] min-h-[48px]"
              style={{ boxShadow: '4px 4px 0 0 #000' }}
            >
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
          <p className="text-xs font-bold text-kinic-text-secondary mt-3 text-center uppercase tracking-wide">
            Conversations are logged on Monad blockchain for transparency
          </p>
        </div>
      </main>
    </div>
  )
}
