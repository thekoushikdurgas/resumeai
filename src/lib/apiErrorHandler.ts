/**
 * API error handling — minimal variant for resume app (no Sonner toasts).
 */

import type { ParsedApiError } from "./apiErrorTypes";
import { toast } from "./toast";

export function showApiErrorToast(error: unknown): void {
  if (error instanceof Error) {
    const parsed = (error as Error & { parsedError?: ParsedApiError }).parsedError;
    if (parsed) {
      toast.error(parsed.message);
      return;
    }
    toast.error(error.message);
    return;
  }
  toast.error("An unexpected error occurred.");
}
