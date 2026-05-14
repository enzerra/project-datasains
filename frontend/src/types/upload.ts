export interface LocalHistoryItem {
  analysisId: string
  label: string
  congestionLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  totalVehicles: number
  analyzedAt: string
}
