interface MemoryCardProps {
  title: string
  summary: string
  tags: string
  timestamp: number
  contentHash: string
}

export default function MemoryCard({ title, summary, tags, timestamp, contentHash }: MemoryCardProps) {
  const date = new Date(timestamp * 1000).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

  const tagList = tags.split(',').filter(Boolean)

  return (
    <div className="card-hover">
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-lg font-black text-kinic-dark uppercase">{title}</h3>
        <span className="text-xs font-bold text-kinic-text-secondary uppercase">{date}</span>
      </div>

      <p className="text-sm font-medium text-kinic-text-secondary mb-4 line-clamp-2">{summary}</p>

      {/* Tags */}
      {tagList.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {tagList.map((tag, i) => (
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

      {/* Content Hash */}
      <div className="text-xs font-mono font-bold text-kinic-text-secondary">
        {contentHash.slice(0, 20)}...
      </div>
    </div>
  )
}
