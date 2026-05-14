'use client'

import { useEffect, useMemo, useRef } from 'react'
import { useParams, useRouter } from 'next/navigation'

import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { PageWrapper } from '@/components/layout/PageWrapper'
import { MetricsPanel } from '@/components/analysis/MetricsPanel'
import { CongestionMap } from '@/components/analysis/CongestionMap'
import { DetectionList } from '@/components/analysis/DetectionList'
import { ExportButton } from '@/components/analysis/ExportButton'
import { ProcessingStatus } from '@/components/analysis/ProcessingStatus'
import { useAnalysis } from '@/hooks/useAnalysis'
import { useLocalHistory } from '@/hooks/useLocalHistory'
import { DownloadCloud } from 'lucide-react'

export default function ResultPage() {
  const params = useParams<{ id: string }>()
  const router = useRouter()
  const { addHistoryItem } = useLocalHistory()
  const label = 'Analisis video lalu lintas'
  const { result, status, progress, annotatedVideoUrl } = useAnalysis(params.id)
  const historySaved = useRef(false)

  const levelLabel = (level?: string) => {
    switch (level?.toLowerCase()) {
      case 'low':
        return 'Rendah'
      case 'medium':
        return 'Sedang'
      case 'high':
        return 'Tinggi'
      case 'critical':
        return 'Kritis'
      default:
        return level ?? '-'
    }
  }

  const congestionVariant = useMemo(() => {
    if (!result) return 'low' as const
    return result.congestion_level.toLowerCase() as 'low' | 'medium' | 'high' | 'critical'
  }, [result])

  useEffect(() => {
    if (status !== 'completed' || !result || historySaved.current) return

    addHistoryItem({
      analysisId: params.id,
      label,
      congestionLevel: result.congestion_level,
      totalVehicles: result.total_vehicles_detected,
      analyzedAt: result.processed_at,
    })
    historySaved.current = true
  }, [addHistoryItem, label, params.id, result, status])

  return (
    <div className="min-h-screen bg-page text-slate-900">
      <Header />
      <PageWrapper>
        <section className="mx-auto max-w-7xl py-10 sm:py-14">
          {status !== 'completed' || !result ? (
            <div className="grid gap-6 lg:grid-cols-[1fr_0.75fr]">
              <Card className="border border-slate-200 bg-white p-6 shadow-sm">
                <ProcessingStatus analysisId={params.id} analysisStatus={status} progress={progress} />
              </Card>
            </div>
          ) : (
            <div className="space-y-8">
              <Card className="border border-slate-200 bg-white p-6 text-slate-900 shadow-sm sm:p-8">
                <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                  <div className="max-w-3xl">
                    <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">Analisis selesai</p>
                    <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight sm:text-4xl">{label}</h1>
                    <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">{result.summary}</p>
                  </div>
                  <Badge variant={congestionVariant}>{levelLabel(result.congestion_level)}</Badge>
                </div>
              </Card>

              <MetricsPanel result={result} />

              {annotatedVideoUrl && (
                <Card className="border border-slate-200 bg-white p-4 shadow-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">Video beranotasi</p>
                  <h2 className="font-display text-lg font-semibold tracking-tight text-slate-900">Video hasil deteksi</h2>
                  <div className="mt-3">
                    <video controls src={annotatedVideoUrl} className="w-full max-h-[480px] bg-black" />
                  </div>
                  <div className="mt-3 flex gap-2">
                    <a href={annotatedVideoUrl} download>
                      <Button className="gap-2">
                        <DownloadCloud className="h-4 w-4" />
                        Unduh video beranotasi
                      </Button>
                    </a>
                  </div>
                </Card>
              )}

              <Card className="border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">Tren waktu</p>
                    <h2 className="font-display text-xl font-semibold tracking-tight text-slate-900">Garis waktu kemacetan</h2>
                  </div>
                  <p className="text-sm text-slate-500">Skor per frame dari hasil Roboflow.</p>
                </div>
                <CongestionMap timeline={result.timeline} />
              </Card>
              <DetectionList result={result} />
              <div className="flex flex-col gap-3 sm:flex-row">
                <ExportButton result={result} />
                <Button variant="secondary" onClick={() => router.push('/')}>Analisis video lain</Button>
              </div>
            </div>
          )}
        </section>
      </PageWrapper>
      <Footer />
    </div>
  )
}