export interface Credentials {
  email: string
  password: string
}

export interface LoginResult {
  accessToken: string
  expiresIn: number
}

export interface UserProfile {
  email: string
  name: string
  role: string
}

export class InvalidCredentialsError extends Error {
  constructor() {
    super('Invalid credentials')
    this.name = 'InvalidCredentialsError'
  }
}

export class UnauthorizedError extends Error {
  constructor() {
    super('Unauthorized')
    this.name = 'UnauthorizedError'
  }
}

interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
}

interface MeResponse {
  email: string
  name: string
  role: string
}

export async function login(credentials: Credentials): Promise<LoginResult> {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  })

  if (response.status === 401) {
    throw new InvalidCredentialsError()
  }

  if (!response.ok) {
    throw new Error('Login request failed')
  }

  const body = (await response.json()) as LoginResponse
  return { accessToken: body.access_token, expiresIn: body.expires_in }
}

export async function fetchProfile(token: string): Promise<UserProfile> {
  const response = await fetch('/api/v1/auth/me', {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (response.status === 401) {
    throw new UnauthorizedError()
  }

  if (!response.ok) {
    throw new Error('Profile request failed')
  }

  const body = (await response.json()) as MeResponse
  return { email: body.email, name: body.name, role: body.role }
}
