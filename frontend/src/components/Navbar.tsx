import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <div className="flex items-baseline gap-2">
        <span className="text-lg font-bold text-brand-700">MedAssist AI</span>
        <span className="text-xs text-slate-400">informational only, not a diagnosis</span>
      </div>
      {user && (
        <div className="flex items-center gap-4 text-sm text-slate-600">
          <span>
            {user.full_name} <span className="text-slate-400">({user.role})</span>
          </span>
          <button
            onClick={logout}
            className="rounded-md border border-slate-300 px-3 py-1 text-slate-700 hover:bg-slate-50"
          >
            Log out
          </button>
        </div>
      )}
    </header>
  );
}
