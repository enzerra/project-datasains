import type { AnalysisResult } from '@/types/analysis'
import { Button } from '@/components/ui/Button'
import { DownloadCloud } from 'lucide-react'

export function ExportButton({ result }: { result: AnalysisResult }) {
  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'analysis-result.json'
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <Button onClick={handleDownload} className="gap-2">
      <DownloadCloud className="h-4 w-4" />
      Unduh laporan JSON
    </Button>
  )
}
