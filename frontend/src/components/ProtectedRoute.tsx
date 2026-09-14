/**
 * Route guard: redirects to /login if nobody's signed in, and to a
 * "not authorized" message if the signed-in user's role isn't allowed
 * on this route -- e.g. a patient hitting /doctor directly by URL.
 */
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { UserRole } from "../api/auth";

export default function ProtectedRoute({
  children,
  allowedRoles,
}: {
  children: React.ReactNode;
  allowedRoles?: UserRole[];
}) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <div className="flex h-screen items-center justify-center text-slate-500">Loading…</div>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-2 text-slate-600">
        <p className="text-lg font-semibold">Not authorized</p>
        <p>Your account ({user.role}) can't access this page.</p>
      </div>
    );
  }
  return <>{children}</>;
}
