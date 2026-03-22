/**
 * Authentication Error Handler
 * Centralized utility for detecting and handling authentication errors.
 */

import type { ParsedApiError } from "./apiErrorTypes";
import { clearTokens } from "./tokenManager";

export function isAuthError(error: unknown): boolean {
  if (error instanceof Error) {
    const message = error.message.toLowerCase();
    return (
      message.includes("authentication failed") ||
      message.includes("please login again") ||
      message.includes("unauthorized") ||
      message.includes("401") ||
      message.includes("token") ||
      message.includes("expired")
    );
  }
  return false;
}

export function extractFieldErrors(error: unknown): Record<string, string[]> {
  if (error instanceof Error) {
    const parsedError = (error as Error & { parsedError?: ParsedApiError })
      .parsedError;
    if (parsedError?.fieldErrors) return parsedError.fieldErrors;
  }
  return {};
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    const parsedError = (error as Error & { parsedError?: ParsedApiError })
      .parsedError;
    if (parsedError) return parsedError.message;
    return error.message;
  }
  return String(error);
}

export function handleAuthError(): void {
  if (typeof window === "undefined") return;
  clearTokens();
  const currentPath = window.location.pathname;
  const loginPath = "/login";
  if (currentPath !== loginPath) {
    try {
      sessionStorage.setItem("redirectAfterLogin", currentPath);
    } catch {
      // ignore
    }
    window.location.href = loginPath;
  }
}

export function checkAndHandleAuthError(error: unknown): boolean {
  if (isAuthError(error)) {
    handleAuthError();
    return true;
  }
  return false;
}

export function handleAuthServiceError(
  error: unknown,
  operation: string,
  _suppressToast = true
): never {
  if (error instanceof Error) {
    const message = error.message;
    if (
      message.includes("401") ||
      message.includes("unauthorized") ||
      message.includes("Authentication failed")
    ) {
      throw new Error("Session expired. Please login again.");
    }
    if (
      operation === "refreshToken" &&
      (message.includes("400") ||
        message.includes("invalid") ||
        message.includes("expired"))
    ) {
      throw new Error("Refresh token expired. Please login again.");
    }
    if (
      message.includes("fetch") ||
      message.includes("network") ||
      message.includes("Failed to fetch")
    ) {
      throw new Error("Network error. Please check your connection.");
    }
  }
  throw error;
}
