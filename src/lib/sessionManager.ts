/**
 * Session Manager - Handles session validation and caching.
 * Validates token presence and expiry; can be extended to call auth.session (01_AUTH) when authService is available.
 */

import { getAccessToken, isTokenExpired } from "./tokenManager";

let lastSessionCheck = 0;
const SESSION_CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes

/**
 * Check if session is valid (token exists and not expired).
 * Does not call API; use authService.getSession() for server-side validation when needed.
 */
export function validateSessionSync(): boolean {
  const token = getAccessToken();
  return token !== null && !isTokenExpired(token);
}

/**
 * Validate session (sync check). Async version can call auth.session when authService exists.
 */
export async function validateSession(): Promise<boolean> {
  return validateSessionSync();
}

/**
 * Check if session check is needed based on last check time.
 */
export function shouldCheckSession(): boolean {
  return Date.now() - lastSessionCheck >= SESSION_CHECK_INTERVAL;
}

/**
 * Reset session check cache.
 */
export function resetSessionCache(): void {
  lastSessionCheck = 0;
}
