import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip as RechartsTooltip, CartesianGrid } from 'recharts'

import type { FrameTimeline } from '@/types/analysis'

function TimelineTooltip({ active, payload }: { active?: boolean; payload?: Array<{ payload?: FrameTimeline }> }) {
  if (!active || !payload?.length) return null

  const frame = payload[0]?.payload
  if (!frame) return null

  return (
    <div className="rounded-md border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">Foto {frame.frame_index + 1}</p>
      <p className="mt-2 text-sm text-slate-600">Waktu: {frame.timestamp_seconds.toFixed(1)}s</p>
      <p className="mt-1 text-sm text-slate-600">Kendaraan: {frame.vehicle_count}</p>
      <p className="mt-1 text-sm text-slate-600">Skor kemacetan: {Math.round(frame.congestion_score * 100)}%</p>
    </div>
  )
}

export function CongestionMap({ timeline }: { timeline: FrameTimeline[] }) {
  return (
    <div className="mt-4 h-80 w-full rounded-md border border-slate-200 bg-white p-4 text-slate-900">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={timeline}>
          <CartesianGrid stroke="#e2e8f0" strokeDasharray="4 4" />
          <XAxis dataKey="frame_index" stroke="#64748b" tickLine={false} axisLine={false} minTickGap={18} />
          <YAxis stroke="#64748b" domain={[0, 1]} tickLine={false} axisLine={false} width={30} />
          <RechartsTooltip content={<TimelineTooltip />} cursor={{ stroke: 'rgba(15,23,36,0.16)', strokeWidth: 1 }} />
          <defs>
            <linearGradient id="congestionFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#111827" stopOpacity={0.22} />
              <stop offset="95%" stopColor="#111827" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <Area type="monotone" dataKey="congestion_score" stroke="#111827" strokeWidth={2.5} fill="url(#congestionFill)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
