/** Parsed API error shape (GraphQL extensions). */

export interface ParsedApiError {
  message: string;
  status: number;
  fieldErrors?: Record<string, string[]>;
  detail?: unknown;
  isValidationError: boolean;
  isPermissionError: boolean;
}
