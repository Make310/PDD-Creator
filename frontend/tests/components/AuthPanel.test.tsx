import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { AuthPanel } from '../../src/components/AuthPanel'
import { fetchProfile, InvalidCredentialsError, login } from '../../src/services/authService'
import { readToken, storeToken } from '../../src/services/tokenStorage'

vi.mock('../../src/services/authService')
vi.mock('../../src/services/tokenStorage')

function fillAndSubmit(email: string, password: string): void {
  if (email) {
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: email } })
  }
  if (password) {
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: password },
    })
  }
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))
}

describe('AuthPanel', () => {
  beforeEach(() => {
    vi.mocked(readToken).mockReturnValue(null)
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('shows the login form when there is no session', async () => {
    render(<AuthPanel />)

    expect(await screen.findByRole('button', { name: 'Sign in' })).toBeDefined()
  })

  it('logs in successfully and shows the user info from /me', async () => {
    vi.mocked(login).mockResolvedValue({ accessToken: 'tok', expiresIn: 3600 })
    vi.mocked(fetchProfile).mockResolvedValue({
      email: 'ada@example.com',
      name: 'Ada Lovelace',
      role: 'admin',
    })

    render(<AuthPanel />)
    await screen.findByRole('button', { name: 'Sign in' })
    fillAndSubmit('ada@example.com', 'secret')

    expect(await screen.findByText('Ada Lovelace')).toBeDefined()
    expect(screen.getByText('ada@example.com')).toBeDefined()
    expect(screen.getByText('admin')).toBeDefined()
    expect(storeToken).toHaveBeenCalledWith('tok', 3600)
  })

  it('shows a single generic message on bad credentials', async () => {
    vi.mocked(login).mockRejectedValue(new InvalidCredentialsError())

    render(<AuthPanel />)
    await screen.findByRole('button', { name: 'Sign in' })
    fillAndSubmit('ada@example.com', 'wrong')

    const alert = await screen.findByRole('alert')
    expect(alert.textContent).toBe('Invalid credentials')
    expect(fetchProfile).not.toHaveBeenCalled()
  })

  it('validates missing fields without calling the service', async () => {
    render(<AuthPanel />)
    await screen.findByRole('button', { name: 'Sign in' })
    fillAndSubmit('', '')

    expect(await screen.findByText('Email is required')).toBeDefined()
    expect(screen.getByText('Password is required')).toBeDefined()
    expect(login).not.toHaveBeenCalled()
  })

  it('validates a malformed email', async () => {
    render(<AuthPanel />)
    await screen.findByRole('button', { name: 'Sign in' })
    fillAndSubmit('not-an-email', 'secret')

    expect(await screen.findByText('Enter a valid email address')).toBeDefined()
    expect(login).not.toHaveBeenCalled()
  })

  it('restores the session from a stored token on mount', async () => {
    vi.mocked(readToken).mockReturnValue('stored-token')
    vi.mocked(fetchProfile).mockResolvedValue({
      email: 'bob@example.com',
      name: 'Bob',
      role: 'user',
    })

    render(<AuthPanel />)

    expect(await screen.findByText('Bob')).toBeDefined()
    expect(fetchProfile).toHaveBeenCalledWith('stored-token')
  })

  it('returns to the login form after logout', async () => {
    vi.mocked(readToken).mockReturnValue('stored-token')
    vi.mocked(fetchProfile).mockResolvedValue({
      email: 'bob@example.com',
      name: 'Bob',
      role: 'user',
    })

    render(<AuthPanel />)
    const logoutButton = await screen.findByRole('button', { name: 'Log out' })
    fireEvent.click(logoutButton)

    await waitFor(() => expect(screen.getByRole('button', { name: 'Sign in' })).toBeDefined())
  })
})
