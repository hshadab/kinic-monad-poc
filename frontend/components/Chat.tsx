'use client'

interface Message {
  role: 'user' | 'assistant'
  content: string
  memories?: Array<{ text: string; score: number; tag: string }>
  monad_tx?: string
}

interface ChatProps {
  messages: Message[]
}

export default function Chat({ messages }: ChatProps) {
  return (
    <div className="space-y-6">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-3xl border-4 border-black p-5 ${
              message.role === 'user'
                ? 'bg-gradient-monad text-white'
                : 'bg-white text-kinic-dark'
            }`}
            style={{ boxShadow: '6px 6px 0 0 #000' }}
          >
            <div className="flex items-start space-x-3">
              {/* Avatar */}
              <div
                className={`w-10 h-10 border-3 border-black flex items-center justify-center flex-shrink-0 ${
                  message.role === 'user'
                    ? 'bg-white'
                    : 'bg-gradient-monad'
                }`}
                style={{ boxShadow: '3px 3px 0 0 #000' }}
              >
                {message.role === 'user' ? (
                  <svg className="w-5 h-5 text-kinic-dark" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                )}
              </div>

              {/* Content */}
              <div className="flex-1">
                <p className="whitespace-pre-wrap font-medium">{message.content}</p>

                {/* Memories Used (for assistant messages) */}
                {message.role === 'assistant' && message.memories && message.memories.length > 0 && (
                  <div className="mt-4 pt-4 border-t-3 border-black">
                    <p className="text-sm font-bold text-kinic-dark mb-3 uppercase">
                      📚 Used {message.memories.length} memories as context:
                    </p>
                    <div className="space-y-2">
                      {message.memories.map((memory, i) => (
                        <div key={i} className="text-sm bg-kinic-light-secondary border-2 border-black p-3">
                          <div className="flex justify-between mb-2">
                            <span className="text-kinic-text-secondary text-xs font-bold uppercase">
                              Relevance: {(memory.score * 100).toFixed(0)}%
                            </span>
                            <span className="text-kinic-cyan text-xs font-bold uppercase">{memory.tag}</span>
                          </div>
                          <p className="text-kinic-dark text-xs line-clamp-2">
                            {memory.text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Monad Transaction */}
                {message.monad_tx && (
                  <div className="mt-3 text-xs font-bold text-kinic-text-secondary flex items-center space-x-2 uppercase">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
                    </svg>
                    <span>Logged on Monad: {message.monad_tx.slice(0, 16)}...</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
