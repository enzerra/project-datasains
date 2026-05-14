import { Card } from '@/components/ui/Card'
import type { AnalysisResult } from '@/types/analysis'

export function DetectionList({ result }: { result: AnalysisResult }) {
  const items = Object.entries(result.vehicle_breakdown)
  return (
    <Card className="border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">Komposisi objek</p>
          <h2 className="font-display text-xl font-semibold tracking-tight text-slate-900">Rincian deteksi</h2>
        </div>
        <p className="text-sm text-slate-500">Jumlah dari frame yang dipilih.</p>
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        {items.map(([label, value]) => (
          <div key={label} className="rounded-md border border-slate-200 bg-slate-50 p-4 text-center shadow-sm">
            <p className="text-sm capitalize text-slate-600">{label}</p>
            <p className="mt-2 font-display text-3xl font-semibold tracking-tight text-slate-900">{value as number}</p>
          </div>
        ))}
      </div>
    </Card>
  )
}
