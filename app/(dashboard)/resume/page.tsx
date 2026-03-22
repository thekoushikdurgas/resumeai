"use client";

import { DashboardAccessGate } from "@/components/shared/DashboardAccessGate";
import App from "@/App";

export default function ResumeDashboardPage() {
  return (
    <DashboardAccessGate pageId="resume">
      <App />
    </DashboardAccessGate>
  );
}
