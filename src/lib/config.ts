/** App configuration (aligns with contact360.io/app pattern). */

export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://api.contact360.io";

export const GRAPHQL_URL =
  process.env.NEXT_PUBLIC_GRAPHQL_URL || `${API_URL}/graphql`;

/** Base URL for resumeai FastAPI (no trailing slash). */
export const RESUME_AI_URL =
  process.env.NEXT_PUBLIC_RESUME_AI_URL || "http://127.0.0.1:8080/v1";

/** Service API key for X-API-Key (must match resumeai API_KEY). */
export const RESUME_AI_API_KEY =
  process.env.NEXT_PUBLIC_RESUME_AI_API_KEY || "";
