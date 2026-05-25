import type { ReactNode } from 'react'

export function PageWrapper({ children }: { children: ReactNode }) {
  return <main className="relative z-10 mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">{children}</main>
}
