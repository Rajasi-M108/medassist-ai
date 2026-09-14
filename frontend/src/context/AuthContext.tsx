/**
 * Holds the logged-in user + token for the whole app, and persists them
 * in localStorage so a page refresh doesn't log the user out.
 *
 * On first load we don't trust a stale cached user blindly -- we
 * re-validate the token against GET /auth/me so a revoked/deactivated
 * account (or an expired token) is caught immediately instead of only
 * on the next API call.
 */
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { User, login as apiLogin, register as apiRegister, fetchMe } from "../api/auth";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<User>;
  register: (email: string, password: string, fullName: string) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("medassist_token");
    if (!token) {
      setIsLoading(false);
      return;
    }
    fetchMe()
      .then((u) => setUser(u))
      .catch(() => {
        localStorage.removeItem("medassist_token");
        localStorage.removeItem("medassist_user");
      })
      .finally(() => setIsLoading(false));
  }, []);

  function persist(token: string, u: User) {
    localStorage.setItem("medassist_token", token);
    localStorage.setItem("medassist_user", JSON.stringify(u));
    setUser(u);
  }

  async function login(email: string, password: string) {
    const res = await apiLogin(email, password);
    persist(res.access_token, res.user);
    return res.user;
  }

  async function register(email: string, password: string, fullName: string) {
    const res = await apiRegister(email, password, fullName);
    persist(res.access_token, res.user);
    return res.user;
  }

  function logout() {
    localStorage.removeItem("medassist_token");
    localStorage.removeItem("medassist_user");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
