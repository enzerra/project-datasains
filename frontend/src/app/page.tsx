'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { ArrowRight } from 'lucide-react'

import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { PageWrapper } from '@/components/layout/PageWrapper'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { VideoDropzone } from '@/components/upload/VideoDropzone'
import { VideoPreview } from '@/components/upload/VideoPreview'
import { UploadProgress } from '@/components/upload/UploadProgress'
import { useVideoUpload } from '@/hooks/useVideoUpload'
import { uploadAndAnalyzeSchema } from '@/lib/constants'

export default function HomePage() {
  const router = useRouter()
  const { upload, status, progress, error } = useVideoUpload()
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleAnalyze = async () => {
    if (!selectedFile) return

    const response = await upload(selectedFile)
    router.push(`/result/${response.analysis_id}`)
  }

  return (
    <div className="min-h-screen bg-page text-slate-900">
      <Header />
      <PageWrapper>
        <section className="mx-auto max-w-2xl space-y-8 py-12 sm:py-16">
          <div className="space-y-4 text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Analisis video lalu lintas</p>
            <h1 className="font-display text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
              Unggah video lalu lintas.
              <br />
              Dapatkan hasil kemacetan.
            </h1>
            <p className="mx-auto max-w-xl text-base leading-7 text-slate-600">
              Sederhana, cepat, dan mudah dipahami. Pilih video lalu jalankan analisis.
            </p>
          </div>

          <Card className="border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
            <div className="space-y-5">
              <VideoDropzone onFileSelected={setSelectedFile} selectedFile={selectedFile} />
              {selectedFile ? <VideoPreview file={selectedFile} /> : null}
              {status === 'uploading' ? <UploadProgress progress={progress} /> : null}
              <Button onClick={handleAnalyze} disabled={!uploadAndAnalyzeSchema.safeParse({ file: selectedFile }).success || status === 'uploading'} className="w-full gap-2 py-3.5">
                {status === 'uploading' ? 'Sedang menganalisis...' : 'Analisis video'}
                <ArrowRight className="h-4 w-4" />
              </Button>
              <p className="text-center text-sm text-slate-500">Setelah mulai, Anda akan diarahkan ke halaman hasil.</p>
              {error ? <p className="text-sm text-danger">{error}</p> : null}
            </div>
          </Card>
        </section>
      </PageWrapper>
      <Footer />
    </div>
  )
}