import { useCallback, useEffect, useState } from 'react'

import { fetchProfile, type UserProfile } from '../services/authService'
import { clearToken, readToken, storeToken } from '../services/tokenStorage'

export type AuthStatus = 'loading' | 'authenticated' | 'unauthenticated'

export interface Auth {
  status: AuthStatus
  user: UserProfile | null
  onAuthenticated: (accessToken: string, expiresIn: number) => void
  logout: () => void
}

export function useAuth(): Auth {
  const [status, setStatus] = useState<AuthStatus>(() =>
    readToken() ? 'loading' : 'unauthenticated',
  )
  const [user, setUser] = useState<UserProfile | null>(null)

  const logout = useCallback(() => {
    clearToken()
    setUser(null)
    setStatus('unauthenticated')
  }, [])

  const loadProfile = useCallback((token: string): void => {
    fetchProfile(token)
      .then((profile) => {
        setUser(profile)
        setStatus('authenticated')
      })
      .catch(() => {
        // Any failure (including an expired/rejected token) drops the session.
        clearToken()
        setUser(null)
        setStatus('unauthenticated')
      })
  }, [])

  const onAuthenticated = useCallback(
    (accessToken: string, expiresIn: number) => {
      storeToken(accessToken, expiresIn)
      setStatus('loading')
      loadProfile(accessToken)
    },
    [loadProfile],
  )

  useEffect(() => {
    const token = readToken()
    if (token) {
      loadProfile(token)
    }
  }, [loadProfile])

  return { status, user, onAuthenticated, logout }
}
