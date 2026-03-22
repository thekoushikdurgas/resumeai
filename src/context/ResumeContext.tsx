"use client";

/**
 * Imperative store for the resume editor (optional consumers / future splits).
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type ResumeEditorApi = Record<string, any>;

let _store: ResumeEditorApi | null = null;

export function setResumeEditorStore(next: ResumeEditorApi): void {
  _store = next;
}

export function useResumeContext(): ResumeEditorApi {
  if (!_store) {
    throw new Error("useResumeContext must run under ResumeEditor");
  }
  return _store;
}
