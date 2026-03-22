/** Minimal toast stub (contact360 uses Sonner; resume app logs to console). */

export const toast = {
  error: (title: string, _opts?: { description?: string; duration?: number }) => {
    if (typeof console !== "undefined") console.error(title);
  },
  warning: (title: string, _opts?: { description?: string; duration?: number }) => {
    if (typeof console !== "undefined") console.warn(title);
  },
  info: (title: string, _opts?: { description?: string; duration?: number }) => {
    if (typeof console !== "undefined") console.info(title);
  },
};
