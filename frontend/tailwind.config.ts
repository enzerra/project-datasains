import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f1724',
          950: '#090d14',
        },
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f1724',
        },
        accent: {
          50: '#f8fafc',
          100: '#f1f5f9',
          300: '#cbd5e1',
          500: '#111827',
          700: '#090d14',
        },
        success: '#16a34a',
        warning: '#f59e0b',
        danger: '#ef4444',
        border: '#e6edf3',
      },
      fontFamily: {
        display: ['var(--font-display)', 'Inter', 'system-ui', 'Segoe UI', 'sans-serif'],
        body: ['var(--font-body)', 'Inter', 'system-ui', 'Segoe UI', 'sans-serif'],
        mono: ['var(--font-mono)', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      boxShadow: {
        sm: '0 1px 2px rgba(16,24,40,0.04)',
        md: '0 6px 18px rgba(16,24,40,0.06)',
      },
      borderRadius: {
        sm: '6px',
        md: '8px',
        lg: '12px',
      },
    },
  },
  plugins: [],
}

export default config
