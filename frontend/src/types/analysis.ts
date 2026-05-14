export type CongestionLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

export interface VehicleBreakdown {
  car: number
  motorcycle: number
  truck: number
  bus: number
  pedestrian: number
}

export interface FrameTimeline {
  frame_index: number
  timestamp_seconds: number
  vehicle_count: number
  congestion_score: number
}

export interface AnalysisResult {
  congestion_level: CongestionLevel
  congestion_score: number
  total_vehicles_detected: number
  vehicle_breakdown: VehicleBreakdown
  average_speed_kmh: number | null
  frames_analyzed: number
  timeline: FrameTimeline[]
  summary: string
  processed_at: string
  processing_duration_ms: number
}

export type AnalysisStatus = 'idle' | 'processing' | 'completed' | 'failed'
