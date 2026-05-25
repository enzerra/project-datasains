import { Progress } from '@/components/ui/Progress'
import { PageWrapper } from '../layout/PageWrapper';

export function ProcessingStatus({ analysisId, analysisStatus, progress }: { analysisId?: string; analysisStatus?: string; progress?: { current_step?: string; steps_completed?: number; steps_total?: number; message?: string } }) {
  const percentage = progress && progress.steps_total ? Math.round(((progress.steps_completed ?? 0) / progress.steps_total) * 100) : analysisStatus === 'completed' ? 100 : 65

return (
        <PageWrapper>
        <section className="mx-auto max-w-2xl space-y-8 py-12 sm:py-16">
    <div className="space-y-4">
      <div className="space-y-2">
        <div className="inline-flex rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-700">
          Analisis berjalan
        </div>
        <p className="font-display text-2xl font-semibold tracking-tight text-slate-900">Sedang memproses foto</p>
        <p className="text-sm leading-6 text-slate-600">Kami sedang menjalankan model deteksi kemacetan pada gambar.</p>
        {analysisId ? <p className="font-mono text-xs text-slate-500">ID analisis: {analysisId}</p> : null}
      </div>

      <div className="space-y-3 rounded-md border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex items-center justify-between text-sm text-slate-600">
          <span className="font-medium text-slate-900">Kemajuan</span>
          <span className="font-mono text-xs uppercase tracking-[0.2em] text-slate-700">{percentage}%</span>
        </div>
        <Progress value={percentage} />
        <p className="text-sm text-slate-500">{progress?.message ?? 'Menyiapkan antrean analisis...'}</p>
      </div>
    </div>
    </section>
    </PageWrapper>
  )
}
