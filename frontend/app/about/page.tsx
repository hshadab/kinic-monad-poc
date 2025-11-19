'use client'

import Nav from '@/components/Nav'

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary">
      <Nav />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-black mb-6 uppercase tracking-tight">
            <span className="text-kinic-dark block mb-2" style={{ textShadow: '4px 4px 0 #23A8E0' }}>How It</span>
            <span className="text-gradient block" style={{ textShadow: '4px 4px 0 rgba(0,0,0,0.1)' }}>Works</span>
          </h1>
          <p className="text-xl font-bold text-kinic-dark max-w-3xl mx-auto">
            The first AI memory agent with dual-blockchain architecture
          </p>
        </div>

        {/* Architecture Overview */}
        <div className="card-brutalist mb-12 bg-white">
          <h2 className="text-3xl font-black text-kinic-dark mb-6 uppercase">Dual-Blockchain Architecture</h2>
          <p className="text-lg font-medium text-kinic-dark mb-6 leading-relaxed">
            This application combines two powerful blockchain networks to create an intelligent,
            transparent memory system that's both cost-effective and verifiable.
          </p>

          <div className="grid md:grid-cols-2 gap-8 mt-8">
            {/* Kinic/IC Side */}
            <div className="border-4 border-black p-6" style={{ boxShadow: '5px 5px 0 0 #23A8E0' }}>
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-kinic-cyan border-3 border-black flex items-center justify-center mr-3">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                </div>
                <h3 className="text-2xl font-black text-kinic-dark uppercase">Kinic/IC</h3>
              </div>
              <h4 className="font-bold text-kinic-dark mb-2 uppercase text-sm">Storage Layer</h4>
              <ul className="space-y-2 text-kinic-dark font-medium">
                <li className="flex items-start">
                  <span className="text-kinic-cyan mr-2 font-black">•</span>
                  <span>Stores full content (notes, documents, conversations)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-kinic-cyan mr-2 font-black">•</span>
                  <span>Generates vector embeddings for semantic search</span>
                </li>
                <li className="flex items-start">
                  <span className="text-kinic-cyan mr-2 font-black">•</span>
                  <span>Finds content by meaning, not just keywords</span>
                </li>
                <li className="flex items-start">
                  <span className="text-kinic-cyan mr-2 font-black">•</span>
                  <span>Cost: ~$0.000001 per operation</span>
                </li>
              </ul>
            </div>

            {/* Monad Side */}
            <div className="border-4 border-black p-6" style={{ boxShadow: '5px 5px 0 0 #FF6B35' }}>
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-kinic-orange border-3 border-black flex items-center justify-center mr-3">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-black text-kinic-dark uppercase">Monad</h3>
              </div>
              <h4 className="font-bold text-kinic-dark mb-2 uppercase text-sm">Metadata & Audit Layer</h4>
              <ul className="space-y-2 text-kinic-dark font-medium">
                <li className="flex items-start">
                  <span className="text-kinic-orange mr-2 font-black">•</span>
                  <span>Logs human-readable metadata (title, summary, tags)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-kinic-orange mr-2 font-black">•</span>
                  <span>Creates searchable, verifiable audit trail</span>
                </li>
                <li className="flex items-start">
                  <span className="text-kinic-orange mr-2 font-black">•</span>
                  <span>Stores content hashes for integrity verification</span>
                </li>
                <li className="flex items-start">
                  <span className="text-kinic-orange mr-2 font-black">•</span>
                  <span>Cost: ~$0.01-0.10 per transaction</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Benefits to Monad Users */}
        <div className="card-brutalist mb-12 bg-gradient-to-br from-kinic-orange to-kinic-pink text-white">
          <h2 className="text-3xl font-black mb-6 uppercase">Benefits to Monad Users</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="border-3 border-white p-5 bg-black/20">
              <h3 className="text-xl font-black mb-3 uppercase flex items-center">
                <span className="text-3xl mr-3">⚡</span>
                High-Speed Transactions
              </h3>
              <p className="font-medium leading-relaxed">
                Monad's 10,000+ TPS means instant memory logging without waiting for slow block times.
                Your knowledge operations are confirmed in seconds, not minutes.
              </p>
            </div>

            <div className="border-3 border-white p-5 bg-black/20">
              <h3 className="text-xl font-black mb-3 uppercase flex items-center">
                <span className="text-3xl mr-3">💰</span>
                Low Gas Costs
              </h3>
              <p className="font-medium leading-relaxed">
                Monad's efficient parallel execution means affordable on-chain logging.
                Store rich metadata (titles, summaries, tags) for ~$0.01-0.10 per operation.
              </p>
            </div>

            <div className="border-3 border-white p-5 bg-black/20">
              <h3 className="text-xl font-black mb-3 uppercase flex items-center">
                <span className="text-3xl mr-3">📖</span>
                Public Knowledge Graph
              </h3>
              <p className="font-medium leading-relaxed">
                Unlike typical blockchains that only store hashes, we log human-readable metadata on Monad.
                Browse your knowledge history directly on-chain via block explorers.
              </p>
            </div>

            <div className="border-3 border-white p-5 bg-black/20">
              <h3 className="text-xl font-black mb-3 uppercase flex items-center">
                <span className="text-3xl mr-3">🔍</span>
                Verifiable Transparency
              </h3>
              <p className="font-medium leading-relaxed">
                Every insert, search, and chat operation creates an immutable record on Monad.
                Prove what you knew and when you knew it - perfect for research, compliance, and IP protection.
              </p>
            </div>

            <div className="border-3 border-white p-5 bg-black/20">
              <h3 className="text-xl font-black mb-3 uppercase flex items-center">
                <span className="text-3xl mr-3">🛠️</span>
                EVM Compatibility
              </h3>
              <p className="font-medium leading-relaxed">
                Standard Solidity smart contracts mean easy integration with existing Ethereum tools.
                Query memories via web3.js, ethers.js, or any Monad RPC endpoint.
              </p>
            </div>

            <div className="border-3 border-white p-5 bg-black/20">
              <h3 className="text-xl font-black mb-3 uppercase flex items-center">
                <span className="text-3xl mr-3">🌐</span>
                Decentralized AI
              </h3>
              <p className="font-medium leading-relaxed">
                Your AI memory context lives on-chain, not in a centralized database.
                Monad's performance makes decentralized AI practical for the first time.
              </p>
            </div>
          </div>
        </div>

        {/* How Data Flows */}
        <div className="card-brutalist mb-12 bg-white">
          <h2 className="text-3xl font-black text-kinic-dark mb-6 uppercase">How Data Flows</h2>

          <div className="space-y-6">
            {/* Insert Flow */}
            <div className="border-l-8 border-kinic-cyan pl-6">
              <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">Inserting a Memory</h3>
              <ol className="space-y-3 text-kinic-dark font-medium">
                <li className="flex">
                  <span className="font-black text-kinic-cyan mr-3">1.</span>
                  <span>You submit content (note, research, document)</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-cyan mr-3">2.</span>
                  <span>AI extracts metadata: title, summary, tags, content hash</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-cyan mr-3">3.</span>
                  <span><strong>Parallel operations:</strong></span>
                </li>
                <li className="flex ml-8">
                  <span className="font-black text-kinic-cyan mr-3">→</span>
                  <span><strong>Kinic/IC:</strong> Stores full content + vector embeddings</span>
                </li>
                <li className="flex ml-8">
                  <span className="font-black text-kinic-orange mr-3">→</span>
                  <span><strong>Monad:</strong> Logs metadata on-chain (title, summary, tags, hash)</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-cyan mr-3">4.</span>
                  <span>Returns: memory ID + blockchain transaction hash</span>
                </li>
              </ol>
            </div>

            {/* Search Flow */}
            <div className="border-l-8 border-kinic-pink pl-6">
              <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">Searching Memories</h3>
              <ol className="space-y-3 text-kinic-dark font-medium">
                <li className="flex">
                  <span className="font-black text-kinic-pink mr-3">1.</span>
                  <span>You enter search query</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-pink mr-3">2.</span>
                  <span><strong>Kinic/IC:</strong> Converts query to vector, finds similar content by <em>meaning</em></span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-pink mr-3">3.</span>
                  <span><strong>Monad:</strong> Logs search operation with query metadata</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-pink mr-3">4.</span>
                  <span>Returns: ranked results by semantic similarity</span>
                </li>
              </ol>
            </div>

            {/* Chat Flow */}
            <div className="border-l-8 border-kinic-yellow pl-6">
              <h3 className="text-2xl font-black text-kinic-dark mb-3 uppercase">AI Chat</h3>
              <ol className="space-y-3 text-kinic-dark font-medium">
                <li className="flex">
                  <span className="font-black text-kinic-yellow mr-3">1.</span>
                  <span>You ask a question</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-yellow mr-3">2.</span>
                  <span>System searches for relevant memories (semantic search)</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-yellow mr-3">3.</span>
                  <span>Claude AI receives question + memory context</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-yellow mr-3">4.</span>
                  <span>AI generates response based on your stored knowledge</span>
                </li>
                <li className="flex">
                  <span className="font-black text-kinic-yellow mr-3">5.</span>
                  <span><strong>Monad:</strong> Logs conversation for audit trail</span>
                </li>
              </ol>
            </div>
          </div>
        </div>

        {/* Why This Matters */}
        <div className="card-brutalist mb-12 bg-gradient-to-br from-kinic-cyan to-kinic-purple text-white">
          <h2 className="text-3xl font-black mb-6 uppercase">Why This Matters</h2>

          <div className="space-y-4 text-lg font-medium leading-relaxed">
            <p>
              <strong className="font-black">For Researchers:</strong> Prove your discoveries and thought processes
              with timestamped, verifiable records on Monad blockchain.
            </p>
            <p>
              <strong className="font-black">For Developers:</strong> Build on top of this memory layer.
              Query the Monad smart contract to access public knowledge graphs and audit trails.
            </p>
            <p>
              <strong className="font-black">For Organizations:</strong> Compliance-ready documentation.
              Every knowledge operation is logged on-chain with human-readable metadata.
            </p>
            <p>
              <strong className="font-black">For AI Enthusiasts:</strong> See how decentralized AI memory works.
              Context lives on-chain, not in centralized databases.
            </p>
            <p>
              <strong className="font-black">For Monad Community:</strong> Demonstrates Monad's unique advantages -
              high throughput enables rich on-chain data that's impractical on slower chains.
            </p>
          </div>
        </div>

        {/* Technical Stats */}
        <div className="card-brutalist bg-white">
          <h2 className="text-3xl font-black text-kinic-dark mb-6 uppercase">Technical Specs</h2>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-6 border-4 border-black" style={{ boxShadow: '4px 4px 0 0 #000' }}>
              <div className="text-4xl font-black text-kinic-cyan mb-2">~2.5s</div>
              <div className="text-sm font-bold text-kinic-dark uppercase">Insert Time</div>
              <div className="text-xs text-kinic-text-secondary mt-1">1.5s IC + 1s Monad</div>
            </div>

            <div className="text-center p-6 border-4 border-black" style={{ boxShadow: '4px 4px 0 0 #000' }}>
              <div className="text-4xl font-black text-kinic-pink mb-2">~1.8s</div>
              <div className="text-sm font-bold text-kinic-dark uppercase">Search Time</div>
              <div className="text-xs text-kinic-text-secondary mt-1">Semantic search + logging</div>
            </div>

            <div className="text-center p-6 border-4 border-black" style={{ boxShadow: '4px 4px 0 0 #000' }}>
              <div className="text-4xl font-black text-kinic-yellow mb-2">$0.01</div>
              <div className="text-sm font-bold text-kinic-dark uppercase">Monad Cost</div>
              <div className="text-xs text-kinic-text-secondary mt-1">Per operation</div>
            </div>
          </div>

          <div className="mt-8 p-6 bg-kinic-light border-3 border-black">
            <h3 className="font-black text-kinic-dark mb-4 uppercase">Smart Contract</h3>
            <div className="font-mono text-sm text-kinic-dark space-y-2">
              <div><span className="font-bold">Address:</span> 0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548</div>
              <div><span className="font-bold">Network:</span> Monad Mainnet</div>
              <div><span className="font-bold">IC Canister:</span> 2x5sz-ciaaa-aaaak-apgta-cai</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-12">
          <a
            href="/chat"
            className="btn-brutalist px-10 py-5 bg-kinic-orange text-white text-lg inline-block"
          >
            Try It Now
          </a>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t-4 border-black py-8 bg-white mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-kinic-text-secondary">
          <p className="font-bold">Built with Kinic, Monad, and Internet Computer</p>
        </div>
      </footer>
    </div>
  )
}
