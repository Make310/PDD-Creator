import { AuthPanel } from './components/AuthPanel'
import { HealthIndicator } from './components/HealthIndicator'

export function App() {
  return (
    <main className="mx-auto max-w-2xl px-4 py-16">
      <h1 className="border-l-4 border-company-yellow pl-4 text-3xl font-semibold text-company-black">
        PDD Creator
      </h1>
      <p className="mt-4 text-company-gray-600">
        Convert RPA process transcripts into structured Process Design Documents.
      </p>
      <div className="mt-8">
        <HealthIndicator />
      </div>
      <div className="mt-8">
        <AuthPanel />
      </div>
    </main>
  )
}
