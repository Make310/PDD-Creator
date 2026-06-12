import { useHealth, type HealthStatus } from '../hooks/useHealth'

const LABELS: Record<HealthStatus, string> = {
  loading: 'Checking API...',
  ok: 'API online',
  error: 'API offline',
}

const STYLES: Record<HealthStatus, string> = {
  loading: 'bg-company-gray-100 text-company-gray-600',
  ok: 'bg-company-yellow/15 text-company-blue',
  error: 'bg-red-50 text-red-700',
}

export function HealthIndicator() {
  const status = useHealth()

  return (
    <span
      data-status={status}
      className={`inline-block rounded-full px-3 py-1 text-sm font-medium ${STYLES[status]}`}
    >
      {LABELS[status]}
    </span>
  )
}
