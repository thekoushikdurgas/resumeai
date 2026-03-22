"use client";

import type { ReactNode } from "react";

/** Simplified gate: full Contact360 gate can replace this later. */
export function DashboardAccessGate({
  children,
}: {
  pageId?: string;
  children: ReactNode;
}) {
  return <>{children}</>;
}
