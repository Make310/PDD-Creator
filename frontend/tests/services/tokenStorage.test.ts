import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { clearToken, readToken, storeToken } from '../../src/services/tokenStorage'

describe('tokenStorage', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  afterEach(() => {
    vi.useRealTimers()
    localStorage.clear()
  })

  it('returns the stored token while it is still valid', () => {
    storeToken('tok', 3600)

    expect(readToken()).toBe('tok')
  })

  it('returns null when no token is stored', () => {
    expect(readToken()).toBeNull()
  })

  it('treats an expired token as absent and clears it', () => {
    vi.useFakeTimers()
    storeToken('tok', 60)

    vi.advanceTimersByTime(61_000)

    expect(readToken()).toBeNull()
    expect(localStorage.getItem('pdd.auth')).toBeNull()
  })

  it('clears the stored token', () => {
    storeToken('tok', 3600)

    clearToken()

    expect(readToken()).toBeNull()
  })

  it('discards a corrupted entry', () => {
    localStorage.setItem('pdd.auth', 'not-json')

    expect(readToken()).toBeNull()
  })
})
