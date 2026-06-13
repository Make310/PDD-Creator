import { useState, type FormEvent } from 'react'

import { useLogin } from '../hooks/useLogin'
import type { LoginResult } from '../services/authService'

interface LoginFormProps {
  onSuccess: (result: LoginResult) => void
}

export function LoginForm({ onSuccess }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { isSubmitting, fieldErrors, formError, submit } = useLogin(onSuccess)

  function handleSubmit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault()
    void submit(email, password)
  }

  return (
    <form noValidate onSubmit={handleSubmit} className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold text-company-black">Sign in</h2>

      {formError && (
        <p role="alert" className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
          {formError}
        </p>
      )}

      <div className="flex flex-col gap-1">
        <label htmlFor="email" className="text-sm font-medium text-company-gray-700">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          aria-invalid={fieldErrors.email ? true : undefined}
          aria-describedby={fieldErrors.email ? 'email-error' : undefined}
          className="rounded-md border border-company-gray-300 px-3 py-2 text-company-black focus:border-company-blue focus:outline-none"
        />
        {fieldErrors.email && (
          <p id="email-error" className="text-sm text-red-700">
            {fieldErrors.email}
          </p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="password" className="text-sm font-medium text-company-gray-700">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          aria-invalid={fieldErrors.password ? true : undefined}
          aria-describedby={fieldErrors.password ? 'password-error' : undefined}
          className="rounded-md border border-company-gray-300 px-3 py-2 text-company-black focus:border-company-blue focus:outline-none"
        />
        {fieldErrors.password && (
          <p id="password-error" className="text-sm text-red-700">
            {fieldErrors.password}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded-md bg-company-yellow px-4 py-2 font-medium text-company-black disabled:opacity-60"
      >
        {isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  )
}
