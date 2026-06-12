import { useEffect, useState } from 'react'

import { fetchHealth } from '../services/healthService'

export type HealthStatus = 'loading' | 'ok' | 'error'

export function useHealth(): HealthStatus {
  const [status, setStatus] = useState<HealthStatus>('loading')

  useEffect(() => {
    let cancelled = false

    fetchHealth()
      .then((ok) => {
        if (!cancelled) setStatus(ok ? 'ok' : 'error')
      })
      .catch(() => {
        if (!cancelled) setStatus('error')
      })

    return () => {
      cancelled = true
    }
  }, [])

  return status
}
