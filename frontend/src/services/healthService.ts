interface HealthResponse {
  ok: boolean
}

export async function fetchHealth(): Promise<boolean> {
  const response = await fetch('/api/v1/health')

  if (!response.ok) {
    return false
  }

  const body = (await response.json()) as HealthResponse
  return body.ok
}
