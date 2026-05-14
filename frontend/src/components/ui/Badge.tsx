import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

const styles = {
  low: 'bg-slate-50 text-slate-700 border border-slate-100',
  medium: 'bg-amber-50 text-amber-700 border border-amber-100',
  high: 'bg-red-50 text-red-700 border border-red-100',
  critical: 'bg-rose-50 text-rose-800 border border-rose-100',
}

export function Badge({ variant = 'low', className, children }: { variant?: keyof typeof styles; className?: string; children: ReactNode }) {
  return <span className={cn('inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium', styles[variant], className)}>{children}</span>
}
