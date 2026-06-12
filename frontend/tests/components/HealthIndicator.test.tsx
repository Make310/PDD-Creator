import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { HealthIndicator } from '../../src/components/HealthIndicator'
import { fetchHealth } from '../../src/services/healthService'

vi.mock('../../src/services/healthService')

describe('HealthIndicator', () => {
  it('shows API online when the health check succeeds', async () => {
    vi.mocked(fetchHealth).mockResolvedValue(true)

    render(<HealthIndicator />)

    expect(await screen.findByText('API online')).toBeDefined()
  })

  it('shows API offline when the health check fails', async () => {
    vi.mocked(fetchHealth).mockRejectedValue(new Error('network down'))

    render(<HealthIndicator />)

    expect(await screen.findByText('API offline')).toBeDefined()
  })
})
