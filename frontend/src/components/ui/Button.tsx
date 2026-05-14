import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

type ButtonVariant = 'primary' | 'secondary' | 'danger'

const variantStyles: Record<ButtonVariant, string> = {
  primary: 'bg-accent-500 text-white shadow-sm hover:bg-accent-700',
  secondary: 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50',
  danger: 'bg-white text-danger border border-slate-200 hover:bg-red-50',
}

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: ButtonVariant }

export function Button({ className, variant, ...props }: Props) {
  const resolvedVariant = variant ?? 'primary'
  return <button className={cn('inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-accent-200 disabled:cursor-not-allowed disabled:opacity-60', variantStyles[resolvedVariant], className)} {...props} />
}
