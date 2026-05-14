'use client'

import { useEffect, useState } from 'react'

import type { LocalHistoryItem } from '@/types/upload'

const storageKey = 'traffic-congestion-history'

export function useLocalHistory() {
  const [history, setHistory] = useState<LocalHistoryItem[]>([])

  useEffect(() => {
    const value = window.localStorage.getItem(storageKey)
    if (value) setHistory(JSON.parse(value) as LocalHistoryItem[])
  }, [])

  const persist = (nextHistory: LocalHistoryItem[]) => {
    setHistory(nextHistory)
    window.localStorage.setItem(storageKey, JSON.stringify(nextHistory))
  }

  const addHistoryItem = (item: LocalHistoryItem) => {
    setHistory((current) => {
      const nextHistory = [item, ...current].slice(0, 20)
      window.localStorage.setItem(storageKey, JSON.stringify(nextHistory))
      return nextHistory
    })
  }

  return { history, addHistoryItem }
}
