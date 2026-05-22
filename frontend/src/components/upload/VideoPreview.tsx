export function VideoPreview({ file }: { file: File }) {
  const duration = 'Unknown'
  return (
    <div className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-slate-900">Foto terpilih</p>
          <p className="text-sm text-slate-600">{file.name}</p>
        </div>
        <div className="text-right text-sm text-slate-500">
          <p>{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
          <p>{duration}</p>
        </div>
      </div>
    </div>
  )
}
