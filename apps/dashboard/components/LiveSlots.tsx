"use client";

import { useEffect, useState } from "react";
import { useNetworkStore } from "@/stores/useNetworkStore";
import { getLatestSlot } from "@/lib/api";

export function LiveSlots() {
  const { latestSlot, slotDelta, connected, setSlot } = useNetworkStore();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function poll() {
      try {
        const data = await getLatestSlot();
        if (!cancelled) {
          setSlot(data.slot);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) setError(String(err));
      }
    }

    poll();
    const id = setInterval(poll, 2000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [setSlot]);

  const delta =
    slotDelta === null ? "" : slotDelta >= 0 ? `+${slotDelta}` : `${slotDelta}`;

  return (
    <div className="rounded-lg border border-slate-800 p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">Latest confirmed slot</p>
        <span
          className={`inline-block h-2 w-2 rounded-full ${
            connected ? "bg-emerald-400" : "bg-slate-500"
          }`}
        />
      </div>
      <p className="text-3xl font-mono mt-2">{latestSlot?.toLocaleString() ?? "—"}</p>
      {slotDelta !== null && (
        <p className="text-xs text-emerald-400 mt-1">{delta} / 2s</p>
      )}
      {error && <p className="text-xs text-red-400 mt-1">{error}</p>}
    </div>
  );
}
