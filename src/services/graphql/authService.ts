/**
 * GraphQL Auth Service (01_AUTH_MODULE).
 * Operations: login, register, logout, refreshToken, session, me.
 * Optional pageType for AuthPayload (role, userType, pages).
 *
 * @see lambda/appointment360/sql/apis/01_AUTH_MODULE.md
 */

import { graphqlMutation, graphqlQuery, gql } from "@/lib/graphqlClient";
import { showApiErrorToast } from "@/lib/apiErrorHandler";
import { handleAuthServiceError } from "@/lib/authErrorHandler";
import type {
  AuthResponse,
  SessionResponse,
  AuthPageType,
  AuthUserProfile,
} from "@/types/auth";

interface GraphQLAuthPayload {
  accessToken: string;
  refreshToken: string;
  user: {
    uuid: string;
    email: string;
    name: string | null;
    role?: string | null;
    userType?: string | null;
  };
  pages?: Array<{
    pageId: string;
    title: string;
    pageType: string;
    route?: string | null;
    status: string;
  }> | null;
}

interface GraphQLSessionInfo {
  userUuid: string;
  email: string;
  isAuthenticated: boolean;
  lastSignInAt: string | null;
}

interface GraphQLMeUser {
  uuid: string;
  email: string;
  name: string | null;
  profile: {
    jobTitle: string | null;
    bio: string | null;
    timezone: string | null;
    avatarUrl: string | null;
    role: string;
    credits: number;
  } | null;
}

function toAuthResponse(payload: GraphQLAuthPayload): AuthResponse {
  return {
    accessToken: payload.accessToken,
    refreshToken: payload.refreshToken,
    user: {
      uuid: payload.user.uuid,
      email: payload.user.email,
      name: payload.user.name ?? undefined,
    },
    role: payload.user.role ?? undefined,
    userType: payload.user.userType ?? undefined,
    pages: payload.pages ?? undefined,
  };
}

export async function login(
  email: string,
  password: string,
  pageType?: AuthPageType
): Promise<AuthResponse> {
  try {
    const mutation = gql`
      mutation Login($input: LoginInput!, $pageType: String) {
        auth {
          login(input: $input, pageType: $pageType) {
            accessToken
            refreshToken
            user {
              uuid
              email
              name
              role
              userType
            }
            pages {
              pageId
              title
              pageType
              route
              status
            }
          }
        }
      }
    `;
    const variables: {
      input: { email: string; password: string };
      pageType?: string;
    } = { input: { email, password } };
    if (pageType) variables.pageType = pageType;

    const response = await graphqlMutation<{
      auth: { login: GraphQLAuthPayload };
    }>(mutation, variables);

    return toAuthResponse(response.auth.login);
  } catch (error) {
    showApiErrorToast(error);
    throw error;
  }
}

export async function register(
  name: string,
  email: string,
  password: string,
  pageType?: AuthPageType
): Promise<AuthResponse> {
  try {
    const mutation = gql`
      mutation Register($input: RegisterInput!, $pageType: String) {
        auth {
          register(input: $input, pageType: $pageType) {
            accessToken
            refreshToken
            user {
              uuid
              email
              name
              role
              userType
            }
            pages {
              pageId
              title
              pageType
              route
              status
            }
          }
        }
      }
    `;
    const variables: {
      input: { name: string; email: string; password: string };
      pageType?: string;
    } = { input: { name, email, password } };
    if (pageType) variables.pageType = pageType;

    const response = await graphqlMutation<{
      auth: { register: GraphQLAuthPayload };
    }>(mutation, variables);

    return toAuthResponse(response.auth.register);
  } catch (error) {
    showApiErrorToast(error);
    throw error;
  }
}

export async function logout(): Promise<void> {
  try {
    const mutation = gql`
      mutation Logout {
        auth {
          logout
        }
      }
    `;
    await graphqlMutation<{ auth: { logout: boolean } }>(mutation);
  } catch {
    // Error swallowed - logout is best-effort
  }
}

export async function getSession(): Promise<SessionResponse> {
  try {
    const query = gql`
      query GetSession {
        auth {
          session {
            userUuid
            email
            isAuthenticated
            lastSignInAt
          }
        }
      }
    `;
    const response = await graphqlQuery<{
      auth: { session: GraphQLSessionInfo | null };
    }>(query);

    if (!response.auth.session) {
      throw new Error("Session expired. Please login again.");
    }

    const session = response.auth.session;
    return {
      user: {
        uuid: session.userUuid,
        email: session.email,
        lastSignInAt: session.lastSignInAt,
      },
    };
  } catch (error) {
    handleAuthServiceError(error, "getSession");
  }
}

export async function getMe(): Promise<AuthUserProfile | null> {
  try {
    const query = gql`
      query GetMe {
        auth {
          me {
            uuid
            email
            name
            profile {
              jobTitle
              bio
              timezone
              avatarUrl
              role
              credits
            }
          }
        }
      }
    `;
    const response = await graphqlQuery<{
      auth: { me: GraphQLMeUser | null };
    }>(query);

    if (!response.auth.me) return null;

    const me = response.auth.me;
    return {
      uuid: me.uuid,
      email: me.email,
      name: me.name ?? "",
      role: me.profile?.role ?? "user",
      avatarUrl: me.profile?.avatarUrl ?? null,
      credits: me.profile?.credits,
      jobTitle: me.profile?.jobTitle ?? null,
      timezone: me.profile?.timezone ?? null,
    };
  } catch (error) {
    handleAuthServiceError(error, "getMe");
  }
}

/**
 * Refresh access token. Optional pageType: when provided, AuthPayload includes role, userType, pages.
 * Uses skipAuth to avoid circular dependency with graphqlClient.
 */
export async function refreshToken(
  pageType?: AuthPageType
): Promise<AuthResponse> {
  try {
    const { getRefreshToken } = await import("@/lib/tokenManager");
    const refreshTokenValue = getRefreshToken();
    if (!refreshTokenValue) {
      throw new Error("No refresh token available");
    }

    const mutation = gql`
      mutation RefreshToken($input: RefreshTokenInput!, $pageType: String) {
        auth {
          refreshToken(input: $input, pageType: $pageType) {
            accessToken
            refreshToken
            user {
              uuid
              email
              name
              role
              userType
            }
            pages {
              pageId
              title
              pageType
              route
              status
            }
          }
        }
      }
    `;
    const variables: {
      input: { refreshToken: string };
      pageType?: string;
    } = { input: { refreshToken: refreshTokenValue } };
    if (pageType) variables.pageType = pageType;

    const response = await graphqlMutation<{
      auth: { refreshToken: GraphQLAuthPayload };
    }>(mutation, variables, { skipAuth: true, showToastOnError: false });

    const payload = response.auth.refreshToken;
    if (!payload.accessToken || !payload.refreshToken) {
      throw new Error("Invalid token response from server");
    }
    return toAuthResponse(payload);
  } catch (error) {
    handleAuthServiceError(error, "refreshToken");
  }
}
