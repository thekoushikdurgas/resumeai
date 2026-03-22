/**
 * GraphQL Client
 * Handles all GraphQL requests with authentication, error handling, and token refresh.
 * Aligns with lambda/appointment360 API (sql/apis/01_AUTH_MODULE.md, README.md).
 */

import { GraphQLClient, gql } from "graphql-request";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
  isTokenExpired,
} from "./tokenManager";
import { checkAndHandleAuthError } from "./authErrorHandler";
import { GRAPHQL_URL } from "./config";
import { showApiErrorToast } from "./apiErrorHandler";

export interface GraphQLRequestOptions {
  skipAuth?: boolean;
  skipRefresh?: boolean;
  showToastOnError?: boolean;
}

let isRefreshing = false;
let refreshPromise: Promise<string | null> | null = null;
const MAX_RETRY_ATTEMPTS = 3;
const INITIAL_RETRY_DELAY = 1000;

export interface GraphQLErrorResponse {
  message: string;
  extensions?: {
    code?: string;
    statusCode?: number;
    fieldErrors?: Record<string, string[]>;
    [key: string]: unknown;
  };
  locations?: Array<{ line: number; column: number }>;
  path?: Array<string | number>;
}

export interface GraphQLResponse<T = unknown> {
  data?: T;
  errors?: GraphQLErrorResponse[];
}

export interface ParsedGraphQLError {
  message: string;
  status: number;
  fieldErrors?: Record<string, string[]>;
  code?: string;
  detail?: string;
  isNotFoundError: boolean;
  isValidationError: boolean;
  isPermissionError: boolean;
}

export function parseGraphQLError(
  errors: GraphQLErrorResponse[]
): ParsedGraphQLError {
  const firstError = errors[0];
  const extensions = firstError?.extensions ?? {};
  const status = (extensions.statusCode as number | undefined) ?? 500;
  const code = (extensions.code as string | undefined) ?? "GRAPHQL_ERROR";
  const fieldErrors = extensions.fieldErrors as
    | Record<string, string[]>
    | undefined;
  let message = firstError?.message ?? "GraphQL request failed";
  const detail =
    typeof extensions.detail === "string"
      ? (extensions.detail as string)
      : message;

  const isNotFoundError =
    status === 404 ||
    code === "NOT_FOUND" ||
    message.toLowerCase().includes("not found");
  const isValidationError =
    status === 400 ||
    status === 422 ||
    (fieldErrors && Object.keys(fieldErrors).length > 0) ||
    code === "VALIDATION_ERROR" ||
    code === "BAD_USER_INPUT";
  const isPermissionError =
    status === 403 || code === "FORBIDDEN" || code === "UNAUTHORIZED";

  if (fieldErrors && Object.keys(fieldErrors).length > 0) {
    const fieldMessages = Object.entries(fieldErrors)
      .map(([field, errs]) => `${field}: ${errs.join(", ")}`)
      .join("; ");
    message = `${message} (${fieldMessages})`;
  }

  return {
    message,
    status,
    fieldErrors,
    code,
    detail,
    isNotFoundError,
    isValidationError,
    isPermissionError,
  };
}

const sleep = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));

function createGraphQLClient(token?: string | null): GraphQLClient {
  const headers: HeadersInit = { "Content-Type": "application/json" };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }
  return new GraphQLClient(GRAPHQL_URL, { headers });
}

async function handleTokenRefresh(retryCount = 0): Promise<string | null> {
  if (isRefreshing && refreshPromise) return refreshPromise;
  isRefreshing = true;
  refreshPromise = (async () => {
    try {
      const refreshTokenValue = getRefreshToken();
      if (!refreshTokenValue || isTokenExpired(refreshTokenValue)) {
        clearTokens();
        return null;
      }
      const mutation = gql`
        mutation RefreshToken($input: RefreshTokenInput!) {
          auth {
            refreshToken(input: $input) {
              accessToken
              refreshToken
            }
          }
        }
      `;
      const refreshClient = createGraphQLClient(null);
      const response = await refreshClient.request<{
        auth: {
          refreshToken: { accessToken: string; refreshToken: string };
        };
      }>(mutation, {
        input: { refreshToken: refreshTokenValue },
      });
      const { accessToken, refreshToken: newRefresh } =
        response.auth?.refreshToken ?? {};
      if (!accessToken || !newRefresh) {
        throw new Error("Invalid token response from server");
      }
      setTokens(accessToken, newRefresh);
      return accessToken;
    } catch (error) {
      if (retryCount < MAX_RETRY_ATTEMPTS) {
        const isNetworkError =
          error instanceof TypeError ||
          (error instanceof Error &&
            (error.message.includes("fetch") ||
              error.message.includes("network") ||
              error.message.includes("Failed to fetch")));
        if (isNetworkError) {
          await sleep(INITIAL_RETRY_DELAY * Math.pow(2, retryCount));
          isRefreshing = false;
          refreshPromise = null;
          return handleTokenRefresh(retryCount + 1);
        }
      }
      const isAuthError =
        error instanceof Error &&
        (error.message.includes("401") ||
          error.message.includes("403") ||
          error.message.includes("invalid") ||
          error.message.includes("expired") ||
          error.message.includes("unauthorized"));
      if (isAuthError || retryCount >= MAX_RETRY_ATTEMPTS) {
        clearTokens();
        return null;
      }
      throw error;
    } finally {
      isRefreshing = false;
      refreshPromise = null;
    }
  })();
  return refreshPromise;
}

export async function graphqlRequest<T = unknown>(
  query: string,
  variables?: Record<string, unknown>,
  options: GraphQLRequestOptions = {}
): Promise<T> {
  const {
    skipAuth = false,
    skipRefresh = false,
    showToastOnError = true,
  } = options;

  try {
    let token: string | null = null;
    if (!skipAuth) {
      token = getAccessToken();
      if (token && isTokenExpired(token) && !skipRefresh) {
        token = await handleTokenRefresh();
      }
    }

    const client = createGraphQLClient(token);

    try {
      const response = await client.request<T>(query, variables);
      return response;
    } catch (error: unknown) {
      if (error && typeof error === "object" && "response" in error) {
        const graphqlError = error as {
          response?: {
            errors?: GraphQLErrorResponse[];
            data?: T;
          };
        };
        const errors = graphqlError.response?.errors ?? [];
        const authError = errors.find(
          (e) =>
            e.extensions?.code === "UNAUTHORIZED" ||
            e.extensions?.statusCode === 401
        );

        if (authError && !skipAuth && !skipRefresh && token) {
          const newToken = await handleTokenRefresh();
          if (newToken) {
            const retryClient = createGraphQLClient(newToken);
            try {
              return await retryClient.request<T>(query, variables);
            } catch (retryError: unknown) {
              if (
                retryError &&
                typeof retryError === "object" &&
                "response" in retryError
              ) {
                const retryResp =
                  (
                    retryError as {
                      response?: { errors?: GraphQLErrorResponse[] };
                    }
                  ).response?.errors ?? [];
                const stillAuth = retryResp.some(
                  (e) =>
                    e.extensions?.code === "UNAUTHORIZED" ||
                    e.extensions?.statusCode === 401
                );
                if (stillAuth) {
                  clearTokens();
                  const err = new Error(
                    "Authentication failed. Please login again."
                  );
                  checkAndHandleAuthError(err);
                  throw err;
                }
              }
              throw retryError;
            }
          } else {
            clearTokens();
            const err = new Error("Authentication failed. Please login again.");
            checkAndHandleAuthError(err);
            throw err;
          }
        }

        if (errors.length > 0) {
          const parsed = parseGraphQLError(errors);
          const apiError = new Error(parsed.message) as Error & {
            parsedError?: ParsedGraphQLError & {
              isValidationError: boolean;
              isPermissionError: boolean;
            };
          };
          apiError.parsedError = {
            ...parsed,
            isValidationError: parsed.isValidationError,
            isPermissionError: parsed.isPermissionError,
          };
          if (showToastOnError) showApiErrorToast(apiError);
          throw apiError;
        }

        if (graphqlError.response?.data) {
          return graphqlError.response.data as T;
        }
      }
      throw error;
    }
  } catch (error) {
    const msg =
      error instanceof Error ? error.message.toLowerCase() : String(error);
    const isNetworkError =
      error instanceof TypeError ||
      msg.includes("fetch") ||
      msg.includes("getaddrinfo") ||
      msg.includes("enotfound") ||
      msg.includes("econnrefused") ||
      msg.includes("network error");
    if (isNetworkError) {
      const networkError = new Error(
        "Network Error: Unable to reach the GraphQL API. Please check your connection and ensure the server is running."
      );
      networkError.name = "NetworkError";
      if (options.showToastOnError !== false) showApiErrorToast(networkError);
      throw networkError;
    }
    throw error;
  }
}

export async function graphqlQuery<T = unknown>(
  query: string,
  variables?: Record<string, unknown>,
  options?: GraphQLRequestOptions
): Promise<T> {
  return graphqlRequest<T>(query, variables, options);
}

export async function graphqlMutation<T = unknown>(
  mutation: string,
  variables?: Record<string, unknown>,
  options?: GraphQLRequestOptions
): Promise<T> {
  return graphqlRequest<T>(mutation, variables, options);
}

export { gql };
