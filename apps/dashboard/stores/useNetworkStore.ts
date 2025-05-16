"use client";

import { create } from "zustand";

interface NetworkState {
  latestSlot: number | null;
  slotDelta: number | null;
  tps: number | null;
  healthScore: number | null;
  connected: boolean;
  connect: () => void;
  disconnect: () => void;
  setSlot: (slot: number) => void;
  setMetrics: (tps: number, score: number) => void;
}

export const useNetworkStore = create<NetworkState>((set, get) => ({
  latestSlot: null,
  slotDelta: null,
  tps: null,
  healthScore: null,
  connected: false,
  connect: () => set({ connected: true }),
  disconnect: () => set({ connected: false }),
  setSlot: (slot) => {
    const prev = get().latestSlot;
    set({
      latestSlot: slot,
      slotDelta: prev === null ? null : slot - prev,
    });
  },
  setMetrics: (tps, score) => set({ tps, healthScore: score }),
}));
