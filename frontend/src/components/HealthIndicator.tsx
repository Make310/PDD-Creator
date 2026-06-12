import { useHealth, type HealthStatus } from '../hooks/useHealth'

const LABELS: Record<HealthStatus, string> = {
  loading: 'Checking API...',
  ok: 'API online',
  error: 'API offline',
}

export function HealthIndicator() {
  const status = useHealth()

  return <span data-status={status}>{LABELS[status]}</span>
}
