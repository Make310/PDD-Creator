import { afterEach, describe, expect, it, vi } from 'vitest'

import {
  fetchProfile,
  InvalidCredentialsError,
  login,
  UnauthorizedError,
} from '../../src/services/authService'

function stubFetch(response: Partial<Response>): ReturnType<typeof vi.fn> {
  const mock = vi.fn().mockResolvedValue(response)
  vi.stubGlobal('fetch', mock)
  return mock
}

describe('login', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('returns the access token and expiry on success', async () => {
    stubFetch({
      ok: true,
      status: 200,
      json: () =>
        Promise.resolve({
          access_token: 'abc',
          token_type: 'bearer',
          expires_in: 3600,
        }),
    })

    const result = await login({ email: 'a@b.com', password: 'secret' })

    expect(result).toEqual({ accessToken: 'abc', expiresIn: 3600 })
  })

  it('posts the credentials to the auth endpoint', async () => {
    const mock = stubFetch({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ access_token: 'abc', token_type: 'bearer', expires_in: 1 }),
    })

    await login({ email: 'a@b.com', password: 'secret' })

    expect(mock).toHaveBeenCalledWith(
      '/api/v1/auth/login',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'a@b.com', password: 'secret' }),
      }),
    )
  })

  it('throws InvalidCredentialsError on 401', async () => {
    stubFetch({ ok: false, status: 401 })

    await expect(login({ email: 'a@b.com', password: 'bad' })).rejects.toBeInstanceOf(
      InvalidCredentialsError,
    )
  })
})

describe('fetchProfile', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('returns the user profile and sends the bearer token', async () => {
    const mock = stubFetch({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ email: 'a@b.com', name: 'Ada', role: 'admin' }),
    })

    const profile = await fetchProfile('token-123')

    expect(profile).toEqual({ email: 'a@b.com', name: 'Ada', role: 'admin' })
    expect(mock).toHaveBeenCalledWith(
      '/api/v1/auth/me',
      expect.objectContaining({
        headers: { Authorization: 'Bearer token-123' },
      }),
    )
  })

  it('throws UnauthorizedError on 401', async () => {
    stubFetch({ ok: false, status: 401 })

    await expect(fetchProfile('expired')).rejects.toBeInstanceOf(UnauthorizedError)
  })
})
