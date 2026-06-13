const STORAGE_KEY = 'pdd.auth'

interface StoredToken {
  accessToken: string
  expiresAt: number
}

export function storeToken(accessToken: string, expiresIn: number): void {
  const stored: StoredToken = {
    accessToken,
    expiresAt: Date.now() + expiresIn * 1000,
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(stored))
}

export function readToken(): string | null {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) {
    return null
  }

  let stored: StoredToken
  try {
    stored = JSON.parse(raw) as StoredToken
  } catch {
    clearToken()
    return null
  }

  if (typeof stored.accessToken !== 'string' || typeof stored.expiresAt !== 'number') {
    clearToken()
    return null
  }

  if (Date.now() >= stored.expiresAt) {
    clearToken()
    return null
  }

  return stored.accessToken
}

export function clearToken(): void {
  localStorage.removeItem(STORAGE_KEY)
}
