"use client";

const NAV_ITEMS: { key: string; label: string }[] = [
  { key: "overview", label: "Overview" },
  { key: "wallets", label: "Wallets" },
  { key: "programs", label: "Programs" },
  { key: "alerts", label: "Alerts" },
];

interface SidebarProps {
  active: string;
  onNavigate: (view: any) => void;
}

export function Sidebar({ active, onNavigate }: SidebarProps) {
  return (
    <aside className="w-56 border-r border-slate-800 p-4 flex flex-col">
      <div className="font-bold text-solana text-lg mb-6">
        <span className="mr-1">🔎</span>SolProbe
      </div>
      <nav className="space-y-1 flex-1">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.key}
            onClick={() => onNavigate(item.key)}
            className={`block w-full text-left rounded px-3 py-2 text-sm transition-colors ${
              active === item.key
                ? "bg-slate-800 text-white"
                : "text-slate-300 hover:bg-slate-800/50"
            }`}
          >
            {item.label}
          </button>
        ))}
      </nav>
      <div className="text-xs text-slate-500 border-t border-slate-800 pt-3">
        v0.1.0 · mainnet-beta
      </div>
    </aside>
  );
}
