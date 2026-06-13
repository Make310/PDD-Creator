import { useState } from 'react'

import { InvalidCredentialsError, login, type LoginResult } from '../services/authService'

export interface FieldErrors {
  email?: string
  password?: string
}

export interface Login {
  isSubmitting: boolean
  fieldErrors: FieldErrors
  formError: string | null
  submit: (email: string, password: string) => Promise<void>
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validate(email: string, password: string): FieldErrors {
  const errors: FieldErrors = {}

  const trimmedEmail = email.trim()
  if (!trimmedEmail) {
    errors.email = 'Email is required'
  } else if (!EMAIL_PATTERN.test(trimmedEmail)) {
    errors.email = 'Enter a valid email address'
  }

  if (!password) {
    errors.password = 'Password is required'
  }

  return errors
}

export function useLogin(onSuccess: (result: LoginResult) => void): Login {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [formError, setFormError] = useState<string | null>(null)

  async function submit(email: string, password: string): Promise<void> {
    setFormError(null)

    const errors = validate(email, password)
    setFieldErrors(errors)
    if (Object.keys(errors).length > 0) {
      return
    }

    setIsSubmitting(true)
    try {
      const result = await login({ email: email.trim(), password })
      onSuccess(result)
    } catch (error) {
      if (error instanceof InvalidCredentialsError) {
        setFormError('Invalid credentials')
      } else {
        setFormError('Something went wrong. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return { isSubmitting, fieldErrors, formError, submit }
}
