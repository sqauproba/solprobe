"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Lightweight WebSocket hook for the API event stream.
 * Reconnects with a fixed delay on disconnect.
 */
export function useSocket(url: string) {
  const [lastMessage, setLastMessage] = useState<any>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let closed = false;

    const open = () => {
      const ws = new WebSocket(url);
      wsRef.current = ws;
      ws.onopen = () => setConnected(true);
      ws.onmessage = (ev) => setLastMessage(JSON.parse(ev.data));
      ws.onclose = () => {
        setConnected(false);
        if (!closed) setTimeout(open, 3000);
      };
    };

    open();
    return () => {
      closed = true;
      wsRef.current?.close();
    };
  }, [url]);

  return { lastMessage, connected };
}
