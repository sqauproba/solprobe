"use client";

import { useEffect, useState } from "react";
import { getHealth } from "@/lib/api";

interface ServiceStatus {
  name: string;
  status: string;
}

export function HealthPanel() {
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [score, setScore] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getHealth();
        setScore(data.score);
        setServices(
          Object.entries(data.services).map(([name, status]) => ({
            name,
            status: String(status),
          }))
        );
        setError(null);
      } catch (err) {
        setError(String(err));
      }
    }
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="rounded-lg border border-slate-800 p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">Platform health</p>
        <span className="font-mono text-sm text-emerald-400">
          {score != null ? `${score}/100` : "—"}
        </span>
      </div>
      <ul className="mt-3 space-y-2">
        {services.map((s) => (
          <li key={s.name} className="flex items-center justify-between text-sm">
            <span className="text-slate-300">{s.name}</span>
            <span
              className={
                s.status === "healthy" ? "text-emerald-400" : "text-red-400"
              }
            >
              {s.status}
            </span>
          </li>
        ))}
      </ul>
      {error && <p className="text-xs text-red-400 mt-2">{error}</p>}
    </div>
  );
}
