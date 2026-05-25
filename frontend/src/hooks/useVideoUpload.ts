'use client'

import { useState } from 'react'
import api from '@/lib/api'

export function useVideoUpload() {
  const [analysisId, setAnalysisId] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState<'idle' | 'uploading' | 'done' | 'error'>('idle')
  const [error, setError] = useState<string | null>(null)

  const upload = async (file: File) => {
    setStatus('uploading')
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post('/api/v1/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (event) => {
          if (!event.total) return
          setProgress(Math.round((event.loaded / event.total) * 100))
        },
      })

      const analysisResponse = await api.post('/api/v1/analyze', { upload_id: response.data.upload_id })
      setAnalysisId(analysisResponse.data.analysis_id)
      setStatus('done')
      return analysisResponse.data
    } catch (caughtError) {
      const message = caughtError instanceof Error ? caughtError.message : 'Unggah gagal'
      setError(message)
      setStatus('error')
      throw caughtError
    }
  }

  const reset = () => {
    setAnalysisId(null)
    setProgress(0)
    setStatus('idle')
    setError(null)
  }

  return { upload, analysisId, progress, status, error, reset }
}
