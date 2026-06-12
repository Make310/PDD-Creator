import { afterEach, describe, expect, it, vi } from 'vitest'

import { fetchHealth } from '../../src/services/healthService'

function stubFetch(response: Partial<Response>): void {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response))
}

describe('fetchHealth', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('returns true when the API responds ok', async () => {
    stubFetch({ ok: true, json: () => Promise.resolve({ ok: true }) })

    const result = await fetchHealth()

    expect(result).toBe(true)
  })

  it('returns false when the API responds with an error status', async () => {
    stubFetch({ ok: false })

    const result = await fetchHealth()

    expect(result).toBe(false)
  })
})
