interface StatsCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  trend?: {
    value: string
    positive: boolean
  }
}

export default function StatsCard({ title, value, icon, trend }: StatsCardProps) {
  return (
    <div className="card-hover">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-bold text-kinic-text-secondary mb-2 uppercase tracking-wide">{title}</p>
          <p className="text-4xl font-black text-kinic-dark">{value}</p>
          {trend && (
            <p className={`text-sm font-bold mt-3 uppercase ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.positive ? '↑' : '↓'} {trend.value}
            </p>
          )}
        </div>
        <div className="w-14 h-14 bg-gradient-monad border-3 border-black flex items-center justify-center" style={{ boxShadow: '4px 4px 0 0 #000' }}>
          {icon}
        </div>
      </div>
    </div>
  )
}
