/**
 * Authentication and session types.
 * Aligned with lambda/appointment360 sql/apis 01_AUTH_MODULE.md (AuthPayload, SessionInfo, UserInfo, PageSummary).
 */

export enum UserRole {
  FREE_USER = "FreeUser",
  PRO_USER = "ProUser",
  ADMIN = "Admin",
  SUPER_ADMIN = "SuperAdmin",
}

export interface UserInfo {
  uuid: string;
  email: string;
  name?: string | null;
}

/** Page summary returned in AuthPayload when pageType is requested (e.g. dashboard). */
export interface PageSummary {
  pageId: string;
  title: string;
  pageType: string;
  route?: string | null;
  status: string;
}

export interface AuthResponse {
  accessToken: string;
  refreshToken: string;
  user: UserInfo;
  role?: string | null;
  userType?: string | null;
  pages?: PageSummary[] | null;
}

export interface SessionResponse {
  user: {
    uuid: string;
    email: string;
    lastSignInAt: string | null;
  };
}

export type AuthPageType = "docs" | "marketing" | "dashboard";

/** Minimal user profile for auth/me and AuthContext (expand in profile page). */
export interface AuthUserProfile {
  uuid: string;
  email: string;
  name: string;
  role: string;
  avatarUrl?: string | null;
  credits?: number;
  jobTitle?: string | null;
  timezone?: string | null;
}
