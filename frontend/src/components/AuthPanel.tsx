import type { ReactNode } from 'react'

import { useAuth, type AuthStatus } from '../hooks/useAuth'
import { LoginForm } from './LoginForm'
import { UserProfileCard } from './UserProfileCard'

export function AuthPanel() {
  const { status, user, onAuthenticated, logout } = useAuth()

  const views: Record<AuthStatus, ReactNode> = {
    loading: <p className="text-company-gray-600">Loading...</p>,
    unauthenticated: (
      <LoginForm onSuccess={(result) => onAuthenticated(result.accessToken, result.expiresIn)} />
    ),
    authenticated: user ? (
      <UserProfileCard user={user} onLogout={logout} />
    ) : (
      <p className="text-company-gray-600">Loading...</p>
    ),
  }

  return (
    <section className="rounded-lg border border-company-gray-200 p-6">{views[status]}</section>
  )
}
