'use client'

import { useEffect, useState } from 'react'

import api from '@/lib/api'
import type { AnalysisResult, AnalysisStatus, AnalysisStatusResponse } from '@/types/analysis'

export function useAnalysis(analysisId: string | null) {
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [status, setStatus] = useState<AnalysisStatus>(analysisId ? 'processing' : 'idle')
  const [progress, setProgress] = useState<{ current_step?: string; steps_completed?: number; steps_total?: number; message?: string } | undefined>()
  const [annotatedImageUrl, setAnnotatedImageUrl] = useState<string | null>(null)

  useEffect(() => {
    if (!analysisId) return

    let active = true
    let interval: ReturnType<typeof setInterval> | undefined

    const fetchStatus = async () => {
      try {
        const { data } = await api.get<AnalysisStatusResponse>(`/api/v1/status/${analysisId}`)
        if (!active) return
        setStatus(data.status)
        setProgress(data.progress ?? undefined)
        if (data.status === 'completed') {
          setResult(data.result ?? null)
          const fallbackUrl = `${api.defaults.baseURL}/api/v1/result/${analysisId}/annotated-image`
          if (data.annotated_image_url) {
            const url = data.annotated_image_url.startsWith('http') ? data.annotated_image_url : `${api.defaults.baseURL}${data.annotated_image_url}`
            setAnnotatedImageUrl(url)
          } else if (data.annotated_video_url) {
            const url = data.annotated_video_url.startsWith('http') ? data.annotated_video_url : `${api.defaults.baseURL}${data.annotated_video_url}`
            setAnnotatedImageUrl(url)
          } else {
            setAnnotatedImageUrl(fallbackUrl)
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

  return { result, status, progress, annotatedImageUrl }
}
