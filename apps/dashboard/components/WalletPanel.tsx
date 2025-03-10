"use client";

import { useState } from "react";
import { getWallet } from "@/lib/api";

/**
 * Wallet lookup panel: enter a Solana address and view balances + activity.
 */
export function WalletPanel() {
  const [address, setAddress] = useState("");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function lookup() {
    if (!address.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const result = await getWallet(address.trim());
      setData(result);
    } catch (err) {
      setError(String(err));
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-lg border border-slate-800 p-4 space-y-4">
      <div className="flex gap-2">
        <input
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && lookup()}
          placeholder="Solana address…"
          className="flex-1 rounded border border-slate-700 bg-slate-900 px-3 py-2 text-sm"
        />
        <button
          onClick={lookup}
          disabled={loading}
          className="rounded bg-solana px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
        >
          {loading ? "…" : "Inspect"}
        </button>
      </div>

      {error && <p className="text-xs text-red-400">{error}</p>}

      {data && (
        <div className="grid grid-cols-3 gap-3 text-sm">
          <div className="rounded border border-slate-800 p-3">
            <p className="text-xs text-slate-500">Address</p>
            <p className="truncate font-mono">{data.address}</p>
          </div>
          <div className="rounded border border-slate-800 p-3">
            <p className="text-xs text-slate-500">SOL balance</p>
            <p className="font-mono">{data.sol_balance}</p>
          </div>
          <div className="rounded border border-slate-800 p-3">
            <p className="text-xs text-slate-500">Lamports</p>
            <p className="font-mono">{data.lamports?.toLocaleString()}</p>
          </div>
        </div>
      )}
    </div>
  );
}
