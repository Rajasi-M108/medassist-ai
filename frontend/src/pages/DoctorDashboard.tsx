import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

export default function DoctorDashboard() {
  const { user } = useAuth();
  return (
    <div>
      <Navbar />
      <main className="mx-auto max-w-4xl px-6 py-8">
        <h1 className="text-xl font-semibold text-slate-800">Welcome, Dr. {user?.full_name}</h1>
        <p className="mt-2 text-sm text-slate-500">
          Your assigned patients and their reports will appear here (coming in the next build phase).
        </p>
      </main>
    </div>
  );
}
