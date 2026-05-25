import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import type { AnalysisResult } from '@/types/analysis'

const items = [
  { label: 'Kendaraan terdeteksi', key: 'total_vehicles_detected', suffix: '' },
  { label: 'Foto dianalisis', key: 'frames_analyzed', suffix: '' },
  { label: 'Skor kemacetan', key: 'congestion_score', suffix: '' },
] as const

export function MetricsPanel({ result }: { result: AnalysisResult }) {
  const levelLabel = (() => {
    switch (result.congestion_level.toLowerCase()) {
      case 'low':
        return 'Rendah'
      case 'medium':
        return 'Sedang'
      case 'high':
        return 'Tinggi'
      case 'critical':
        return 'Kritis'
      default:
        return result.congestion_level
    }
  })()

  return (
    <div className="space-y-4">
      <Card className="border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">Hasil sistem</p>
            <h3 className="font-display text-2xl font-semibold tracking-tight">Kemacetan {levelLabel}</h3>
            <p className="text-sm leading-6 text-slate-600">{result.summary}</p>
          </div>
          <Badge variant={result.congestion_level.toLowerCase() as 'low' | 'medium' | 'high' | 'critical'}>{levelLabel}</Badge>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
            <div className="mt-3 flex items-end justify-between gap-4">
              <div>
                <p className="font-display text-5xl font-semibold leading-none">{Math.round(result.congestion_score * 100)}</p>
                <p className="mt-2 text-sm text-slate-600">Tingkat keparahan dari foto yang diunggah</p>
              </div>
              <div className="w-36 rounded-full bg-slate-200 p-1">
                <div className="h-2 rounded-full bg-slate-900" style={{ width: `${Math.min(100, Math.max(0, result.congestion_score * 100))}%` }} />
              </div>
            </div>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {items.map((item) => {
              const rawValue = result[item.key]
              const value = item.key === 'congestion_score' ? `${Math.round(result.congestion_score * 100)}%` : `${rawValue}${item.suffix}`

              return (
                <div key={item.label} className="rounded-md border border-slate-200 bg-white p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">{item.label}</p>
                  <p className="mt-3 font-display text-2xl font-semibold tracking-tight text-slate-900">{value}</p>
                </div>
              )
            })}
          </div>
        </div>
      </Card>
    </div>
  )
}
