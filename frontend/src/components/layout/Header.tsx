import Image from 'next/image'
import Link from 'next/link'

export function Header() {
  return (
    <header className="sticky top-0 z-20 bg-white/0 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link href="/" className="group flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl bg-white shadow-[0_10px_30px_rgba(0,0,0,0.12)] ring-1 ring-black/10">
            <Image src="/logoproject.png" alt="Logo Prediktor Lalu Lintas" width={40} height={40} className="h-10 w-10 object-cover" priority />
          </span>
          <span className="leading-tight">
            <span className="block font-display text-base font-semibold tracking-tight text-slate-900">Prediktor Lalu Lintas</span>
            <span className="block text-xs text-slate-500">Video ke analisis kemacetan</span>
          </span>
        </Link>
        <nav className="flex items-center gap-3 text-sm">
          <Link href="/history" className="rounded-md px-3 py-1.5 text-slate-700 hover:bg-slate-50">Riwayat</Link>
          <Link href="/" className="rounded-md bg-accent-500 px-3 py-1.5 text-white hover:bg-accent-700">Unggah</Link>
        </nav>
      </div>
    </header>
  )
}
