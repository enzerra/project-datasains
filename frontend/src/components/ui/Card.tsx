import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

export function Card({ className, children }: { className?: string; children: ReactNode }) {
  return <section className={cn('relative overflow-hidden rounded-md bg-white shadow-sm ring-1 ring-slate-100', className)}>{children}</section>
}
