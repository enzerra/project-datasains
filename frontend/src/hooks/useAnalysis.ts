'use client'

import { useEffect, useState } from 'react'

import api from '@/lib/api'
import type { AnalysisResult, AnalysisStatus } from '@/types/analysis'

export function useAnalysis(analysisId: string | null) {
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [status, setStatus] = useState<AnalysisStatus>(analysisId ? 'processing' : 'idle')
  const [progress, setProgress] = useState<{ current_step?: string; steps_completed?: number; steps_total?: number; message?: string } | undefined>()
  const [annotatedVideoUrl, setAnnotatedVideoUrl] = useState<string | null>(null)

  useEffect(() => {
    if (!analysisId) return

    let active = true
    let interval: ReturnType<typeof setInterval> | undefined

    const fetchStatus = async () => {
      try {
        const { data } = await api.get(`/api/v1/status/${analysisId}`)
        if (!active) return
        setStatus(data.status)
        setProgress(data.progress)
        if (data.status === 'completed') {
          setResult(data.result)
          // annotated video URL may be provided on the status response
          if (data.annotated_video_url) {
            const url = data.annotated_video_url.startsWith('http') ? data.annotated_video_url : `${api.defaults.baseURL}${data.annotated_video_url}`
            setAnnotatedVideoUrl(url)
          }

          if (interval) clearInterval(interval)
        }
        if (data.status === 'failed') {
          if (interval) clearInterval(interval)
        }
      } catch {
        if (active) setStatus('failed')
      }
    }

    void fetchStatus()
    interval = setInterval(fetchStatus, 2000)

    return () => {
      active = false
      if (interval) clearInterval(interval)
    }
  }, [analysisId])

  return { result, status, progress, annotatedVideoUrl }
}
