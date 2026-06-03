import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import { Inter, JetBrains_Mono } from 'next/font/google'

import './globals.css'
import { Providers } from '@/components/layout/Providers'

const display = Inter({ subsets: ['latin'], variable: '--font-display', weight: ['400','600','700'] })
const body = Inter({ subsets: ['latin'], variable: '--font-body', weight: ['300','400','600'] })
const mono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' })

export const metadata: Metadata = {
  title: 'Deteksi Kemacetan Lalu Lintas',
  description: 'Unggah foto lalu lintas dan analisis kemacetan dengan computer vision.',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable}`}>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
