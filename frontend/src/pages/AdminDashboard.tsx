import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

export default function AdminDashboard() {
  const { user } = useAuth();
  return (
    <div>
      <Navbar />
      <main className="mx-auto max-w-4xl px-6 py-8">
        <h1 className="text-xl font-semibold text-slate-800">Welcome, {user?.full_name}</h1>
        <p className="mt-2 text-sm text-slate-500">
          User account management and doctor/patient assignment will appear here (coming in the next build phase).
        </p>
      </main>
    </div>
  );
}
