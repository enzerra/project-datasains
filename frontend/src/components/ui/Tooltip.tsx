import type { ReactNode } from 'react'

export function Tooltip({ children }: { children: ReactNode }) {
  return <span title="Information">{children}</span>
}
