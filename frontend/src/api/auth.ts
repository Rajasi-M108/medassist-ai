import { api } from "./client";

export type UserRole = "patient" | "doctor" | "admin";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>("/auth/login", { email, password });
  return data;
}

export async function register(
  email: string,
  password: string,
  full_name: string
): Promise<AuthResponse> {
  // Self-registration always creates a patient account -- the backend
  // rejects any other role here (doctor/admin accounts are provisioned
  // by an administrator).
  const { data } = await api.post<AuthResponse>("/auth/register", {
    email,
    password,
    full_name,
    role: "patient",
  });
  return data;
}

export async function fetchMe(): Promise<User> {
  const { data } = await api.get<User>("/auth/me");
  return data;
}
