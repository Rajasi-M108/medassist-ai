/**
 * One shared axios instance for the whole app.
 *
 * The request interceptor attaches the JWT (if we have one) to every
 * call automatically, and the response interceptor bounces the user
 * back to /login on a 401 -- so individual pages never have to think
 * about auth headers or expired-token handling themselves.
 */
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("medassist_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("medassist_token");
      localStorage.removeItem("medassist_user");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);
