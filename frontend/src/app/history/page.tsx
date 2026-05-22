'use client'

import Link from 'next/link'
import { ArrowLeft, History as HistoryIcon } from 'lucide-react'

import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { PageWrapper } from '@/components/layout/PageWrapper'
import { useLocalHistory } from '@/hooks/useLocalHistory'

export default function HistoryPage() {
  const { history } = useLocalHistory()

  const levelLabel = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low':
        return 'Rendah'
      case 'medium':
        return 'Sedang'
      case 'high':
        return 'Tinggi'
      case 'critical':
        return 'Kritis'
      default:
        return level
    }
  }

  return (
    <div className="min-h-screen bg-page text-slate-900">
      <Header />
      <PageWrapper>
        <section className="mx-auto max-w-5xl py-10 sm:py-14">
          <Card className="border border-slate-200 bg-white p-6 text-slate-900 shadow-sm sm:p-8">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <p className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-500">
                  <HistoryIcon className="h-3.5 w-3.5" />
                  Arsip lokal
                </p>
                <h1 className="mt-4 font-display text-3xl font-semibold tracking-tight sm:text-4xl">Riwayat analisis</h1>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">Analisis terakhir disimpan di browser agar mudah dibuka lagi.</p>
              </div>
              <Link className="inline-flex items-center gap-2 rounded-md border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:bg-slate-50" href="/">
                <ArrowLeft className="h-4 w-4" />
                Kembali ke unggah
              </Link>
            </div>
          </Card>

          <div className="mt-8 space-y-4">
            {history.length === 0 ? (
              <Card className="border border-dashed border-slate-200 bg-white p-8 text-center shadow-sm">
                <p className="text-lg font-medium text-slate-900">Belum ada analisis</p>
                <p className="mt-2 text-sm text-slate-600">Unggah foto pertama untuk melihat hasil di sini.</p>
                <Link className="mt-6 inline-flex rounded-md bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-sm" href="/">Unggah foto</Link>
              </Card>
            ) : (
              history.map((item) => (
                <Card key={item.analysisId} className="border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="font-display text-lg font-semibold tracking-tight text-slate-900">{item.label}</p>
                      <p className="text-sm text-slate-500">{new Date(item.analyzedAt).toLocaleString()}</p>
                      <p className="mt-1 text-xs uppercase tracking-[0.24em] text-slate-500">{item.analysisId}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge variant={item.congestionLevel.toLowerCase() as 'low' | 'medium' | 'high' | 'critical'}>{levelLabel(item.congestionLevel)}</Badge>
                      <Link className="text-sm font-semibold text-slate-900 transition hover:text-slate-600" href={`/result/${item.analysisId}`}>Buka hasil</Link>
                    </div>
                  </div>
                </Card>
              ))
            )}
          </div>
        </section>
      </PageWrapper>
      <Footer />
    </div>
  )
}