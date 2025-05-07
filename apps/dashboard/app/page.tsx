"use client";

import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { LiveSlots } from "@/components/LiveSlots";
import { HealthPanel } from "@/components/HealthPanel";
import { NetworkChart } from "@/components/NetworkChart";
import { EventFeed } from "@/components/EventFeed";
import { WalletPanel } from "@/components/WalletPanel";

type View = "overview" | "wallets" | "programs" | "alerts";

export default function Home() {
  const [view, setView] = useState<View>("overview");

  return (
    <main className="flex min-h-screen">
      <Sidebar active={view} onNavigate={setView} />
      <section className="flex-1 p-6 space-y-6">
        <header>
          <h1 className="text-2xl font-bold">SolProbe</h1>
          <p className="text-sm text-slate-400">
            Real-time Solana observability, diagnostics, and alerting
          </p>
        </header>

        {view === "overview" && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <LiveSlots />
              <HealthPanel />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <NetworkChart title="RPC latency (ms)" metric="rpc_latency_ms" />
              <NetworkChart title="TPS" metric="tps" />
            </div>
            <EventFeed />
          </>
        )}

        {view === "wallets" && <WalletPanel />}

        {view === "programs" && (
          <div className="rounded-lg border border-slate-800 p-4 text-sm text-slate-300">
            Program explorer coming soon.
          </div>
        )}

        {view === "alerts" && (
          <div className="rounded-lg border border-slate-800 p-4 text-sm text-slate-300">
            Alert rules and delivery status coming soon.
          </div>
        )}
      </section>
    </main>
  );
}
