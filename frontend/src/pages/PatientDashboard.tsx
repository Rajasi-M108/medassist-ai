import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

// Placeholder for phase 3 (report upload/list) -- proves the
// role-based routing + auth works end-to-end; real content lands
// once the upload/storage endpoints exist.
export default function PatientDashboard() {
  const { user } = useAuth();
  return (
    <div>
      <Navbar />
      <main className="mx-auto max-w-4xl px-6 py-8">
        <h1 className="text-xl font-semibold text-slate-800">Welcome, {user?.full_name}</h1>
        <p className="mt-2 text-sm text-slate-500">
          Your uploaded reports, AI summaries, and chat will appear here (coming in the next build phase).
        </p>
      </main>
    </div>
  );
}
