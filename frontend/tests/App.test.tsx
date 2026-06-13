import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { App } from '../src/App'
import { fetchProfile } from '../src/services/authService'
import { readToken } from '../src/services/tokenStorage'

vi.mock('../src/services/authService')
vi.mock('../src/services/tokenStorage')

describe('App', () => {
  beforeEach(() => {
    vi.mocked(readToken).mockReturnValue(null)
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('opens on the login experience when unauthenticated', async () => {
    render(<App />)

    expect(await screen.findByRole('button', { name: 'Sign in' })).toBeDefined()
  })

  it('does not show the boilerplate scaffold or a health indicator', async () => {
    render(<App />)
    await screen.findByRole('button', { name: 'Sign in' })

    expect(
      screen.queryByText(
        'Convert RPA process transcripts into structured Process Design Documents.',
      ),
    ).toBeNull()
    expect(screen.queryByText(/API online/)).toBeNull()
    expect(screen.queryByText(/API offline/)).toBeNull()
  })

  it('shows the user profile and logout when authenticated', async () => {
    vi.mocked(readToken).mockReturnValue('stored-token')
    vi.mocked(fetchProfile).mockResolvedValue({
      email: 'ada@example.com',
      name: 'Ada Lovelace',
      role: 'admin',
    })

    render(<App />)

    expect(await screen.findByText('Ada Lovelace')).toBeDefined()
    expect(screen.getByText('ada@example.com')).toBeDefined()
    expect(screen.getByText('admin')).toBeDefined()
    expect(screen.getByRole('button', { name: 'Log out' })).toBeDefined()
  })
})
