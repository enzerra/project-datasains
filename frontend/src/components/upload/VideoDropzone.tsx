'use client'

import { useDropzone } from 'react-dropzone'
import { CloudUpload, FileImage, Image as ImageIcon, ShieldCheck, X } from 'lucide-react'

import { cn } from '@/lib/utils'

export function VideoDropzone({ onFileSelected, selectedFile }: { onFileSelected: (file: File | null) => void; selectedFile: File | null }) {
  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    accept: { 'image/*': [] },
    maxSize: 100 * 1024 * 1024,
    multiple: false,
    onDrop: (acceptedFiles) => onFileSelected(acceptedFiles[0] ?? null),
  })

  const hasError = fileRejections.length > 0

  return (
    <div
      {...getRootProps()}
      className={cn(
        'group cursor-pointer rounded-md border border-slate-200 bg-white p-6 text-center shadow-sm transition-colors duration-150',
        isDragActive ? 'border-accent-500 bg-slate-50' : 'hover:border-slate-300 hover:bg-slate-50',
        hasError ? 'border-danger bg-red-50' : '',
      )}
    >
      <input {...getInputProps()} />
      <div className="mx-auto flex max-w-md flex-col items-center gap-4">
        <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-700">
          <ShieldCheck className="h-3.5 w-3.5" />
          Jalur unggah aman
        </div>
        <div className="rounded-2xl bg-accent-500 p-4 text-white shadow-sm">
          {selectedFile ? <FileImage className="h-7 w-7" /> : <CloudUpload className="h-7 w-7" />}
        </div>
        <div>
          <p className="font-display text-xl font-semibold tracking-tight text-slate-900">
            {selectedFile ? selectedFile.name : 'Tarik foto di sini'}
          </p>
          <p className="mt-2 text-sm leading-6 text-slate-600">Seret file atau klik untuk memilih foto.</p>
        </div>
        {selectedFile ? (
          <div className="flex flex-wrap items-center justify-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-xs text-slate-600">
            <ImageIcon className="h-3.5 w-3.5 text-slate-700" />
            Siap dianalisis
            <span>·</span>
            {Math.round(selectedFile.size / (1024 * 1024))} MB
            <button type="button" onClick={(event) => { event.stopPropagation(); onFileSelected(null) }} className="inline-flex items-center gap-1 font-semibold text-slate-900 hover:text-slate-700">
              <X className="h-3.5 w-3.5" />
              Hapus
            </button>
          </div>
        ) : null}
      </div>
      {hasError ? <p className="mt-4 text-sm font-medium text-danger">Format file tidak didukung atau ukuran terlalu besar. Gunakan foto JPG, PNG, atau WEBP.</p> : null}
    </div>
  )
}
