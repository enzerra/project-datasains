export interface ApiErrorResponse {
  detail: string
}

export interface UploadResponse {
  upload_id: string
  filename: string
  size_bytes: number
  duration_seconds: number
  status: string
  created_at: string
}

export interface AnalyzeResponse {
  analysis_id: string
  upload_id: string
  status: string
  estimated_seconds?: number
}

export interface AnalysisStatusResponse {
  analysis_id: string
  upload_id: string
  status: string
  estimated_seconds?: number
  progress?: { current_step?: string; steps_completed?: number; steps_total?: number; message?: string }
  result?: any
  annotated_video_url?: string
}
