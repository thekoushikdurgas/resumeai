"use client";

/**
 * Auth context: user, login, register, logout, token refresh. Wrap app with AuthProvider; use useAuth() in pages.
 * @module context/AuthContext
 */
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import {
  login as loginService,
  register as registerService,
  logout as logoutService,
  getMe,
  refreshToken as refreshTokenService,
} from "@/services/graphql/authService";
import {
  setTokens,
  clearTokens,
  getAccessToken,
  isTokenExpired,
  isAuthenticated,
} from "@/lib/tokenManager";
import { resetSessionCache } from "@/lib/sessionManager";
import { type AuthUserProfile, type PageSummary, UserRole } from "@/types/auth";

export type AuthUser = AuthUserProfile & { role: UserRole };

interface AuthContextType {
  user: AuthUser | null;
  authPages: PageSummary[] | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function mapRoleToEnum(role: string): UserRole {
  switch (role) {
    case "FreeUser":
      return UserRole.FREE_USER;
    case "ProUser":
      return UserRole.PRO_USER;
    case "Admin":
      return UserRole.ADMIN;
    case "SuperAdmin":
      return UserRole.SUPER_ADMIN;
    default:
      return UserRole.FREE_USER;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [authPages, setAuthPages] = useState<PageSummary[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const hasRestoredAuthPagesRef = useRef(false);

  const loadUser = useCallback(async () => {
    if (!isAuthenticated()) {
      setIsLoading(false);
      return;
    }
    try {
      const profile = await getMe();
      if (profile) {
        setUser({
          ...profile,
          role: mapRoleToEnum(profile.role),
        });
      }
    } catch {
      clearTokens();
      setUser(null);
      setAuthPages(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  useEffect(() => {
    if (
      !isAuthenticated() ||
      user === null ||
      authPages !== null ||
      hasRestoredAuthPagesRef.current
    ) {
      return;
    }
    hasRestoredAuthPagesRef.current = true;
    refreshTokenService("dashboard")
      .then((response) => {
        setAuthPages(response.pages ?? null);
        if (response.role && user) {
          setUser((prev) =>
            prev ? { ...prev, role: mapRoleToEnum(response.role!) } : prev
          );
        }
      })
      .catch(() => {
        hasRestoredAuthPagesRef.current = false;
      });
  }, [user, authPages]);

  useEffect(() => {
    const checkAndRefreshToken = async () => {
      const token = getAccessToken();
      if (token && isTokenExpired(token)) {
        try {
          const response = await refreshTokenService("dashboard");
          setTokens(response.accessToken, response.refreshToken);
          setAuthPages(response.pages ?? null);
          if (response.role && response.user) {
            setUser({
              uuid: response.user.uuid,
              email: response.user.email,
              name: response.user.name ?? "",
              role: mapRoleToEnum(response.role),
              avatarUrl: null,
              credits: 0,
            });
          }
          resetSessionCache();
        } catch {
          clearTokens();
          setUser(null);
          setAuthPages(null);
        }
      }
    };
    checkAndRefreshToken();
    const interval = setInterval(checkAndRefreshToken, 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setError(null);
    try {
      const response = await loginService(email, password, "dashboard");
      setTokens(response.accessToken, response.refreshToken);
      setAuthPages(response.pages ?? null);
      setUser({
        uuid: response.user.uuid,
        email: response.user.email,
        name: response.user.name ?? "",
        role: response.role ? mapRoleToEnum(response.role) : UserRole.FREE_USER,
        avatarUrl: null,
        credits: 0,
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Login failed";
      setError(message);
      throw err;
    }
  }, []);

  const register = useCallback(
    async (name: string, email: string, password: string) => {
      setError(null);
      try {
        const response = await registerService(
          name,
          email,
          password,
          "dashboard"
        );
        setTokens(response.accessToken, response.refreshToken);
        setAuthPages(response.pages ?? null);
        setUser({
          uuid: response.user.uuid,
          email: response.user.email,
          name: response.user.name ?? "",
          role: response.role
            ? mapRoleToEnum(response.role)
            : UserRole.FREE_USER,
          avatarUrl: null,
          credits: 0,
        });
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Registration failed";
        setError(message);
        throw err;
      }
    },
    []
  );

  const logout = useCallback(async () => {
    try {
      await logoutService();
    } finally {
      clearTokens();
      setUser(null);
      setAuthPages(null);
      setError(null);
    }
  }, []);

  const refreshUser = useCallback(async () => {
    if (!isAuthenticated()) return;
    try {
      const profile = await getMe();
      if (profile) {
        setUser({
          ...profile,
          role: mapRoleToEnum(profile.role),
        });
      }
    } catch {
      clearTokens();
      setUser(null);
      setAuthPages(null);
    }
  }, []);

  const clearError = useCallback(() => setError(null), []);

  return (
    <AuthContext.Provider
      value={{
        user,
        authPages,
        isLoading,
        isAuthenticated: !!user,
        error,
        login,
        register,
        logout,
        refreshUser,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
