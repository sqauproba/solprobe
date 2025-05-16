"use client";

import { useSocket } from "@/hooks/useSocket";

interface EventItem {
  id: string;
  kind: string;
  detail: string;
  ts: string;
}

/**
 * Renders the latest events relayed over the API WebSocket stream.
 */
export function EventFeed() {
  const { lastMessage, connected } = useSocket(
    process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8080/v1/stream"
  );

  const events: EventItem[] = lastMessage
    ? [
        {
          id: String(lastMessage.slot ?? Date.now()),
          kind: lastMessage.type ?? "slot",
          detail: lastMessage.slot
            ? `slot ${lastMessage.slot.toLocaleString()}`
            : JSON.stringify(lastMessage),
          ts: new Date().toLocaleTimeString(),
        },
      ]
    : [];

  return (
    <div className="rounded-lg border border-slate-800 p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">Live event feed</p>
        <span
          className={`inline-block h-2 w-2 rounded-full ${
            connected ? "bg-emerald-400" : "bg-slate-500"
          }`}
        />
      </div>
      <ul className="mt-3 space-y-2">
        {events.length === 0 && (
          <li className="text-xs text-slate-500">No events yet</li>
        )}
        {events.map((e) => (
          <li
            key={e.id}
            className="flex items-center justify-between text-sm border-b border-slate-800 pb-1"
          >
            <span className="text-slate-300">
              <span className="text-solana mr-2">{e.kind}</span>
              {e.detail}
            </span>
            <span className="text-xs text-slate-500">{e.ts}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
