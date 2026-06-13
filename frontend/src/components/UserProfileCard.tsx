import type { UserProfile } from '../services/authService'

interface UserProfileCardProps {
  user: UserProfile
  onLogout: () => void
}

export function UserProfileCard({ user, onLogout }: UserProfileCardProps) {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold text-company-black">Signed in</h2>

      <dl className="flex flex-col gap-2 text-company-gray-700">
        <div className="flex gap-2">
          <dt className="font-medium text-company-gray-600">Name</dt>
          <dd>{user.name}</dd>
        </div>
        <div className="flex gap-2">
          <dt className="font-medium text-company-gray-600">Email</dt>
          <dd>{user.email}</dd>
        </div>
        <div className="flex gap-2">
          <dt className="font-medium text-company-gray-600">Role</dt>
          <dd>{user.role}</dd>
        </div>
      </dl>

      <button
        type="button"
        onClick={onLogout}
        className="self-start rounded-md border border-company-gray-300 px-4 py-2 font-medium text-company-black"
      >
        Log out
      </button>
    </div>
  )
}
