import { Progress } from '@/components/ui/Progress'

export function UploadProgress({ progress }: { progress: number }) {
  return (
    <div className="space-y-3 rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between text-sm text-slate-600">
        <span className="font-medium text-slate-900">Mengunggah video</span>
        <span className="font-mono text-xs uppercase tracking-[0.2em] text-slate-700">{progress}%</span>
      </div>
      <Progress value={progress} />
    </div>
  )
}
