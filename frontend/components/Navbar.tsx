'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, MonitorPlay, LogOut } from 'lucide-react';

interface NavbarProps {
  onOpenOnboard?: () => void;
  onOpenShift?: () => void;
}

export default function Navbar({ onOpenOnboard, onOpenShift }: NavbarProps) {
  const pathname = usePathname();

  return (
    <header className="glass-nav sticky top-0 z-40 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-black text-xl text-white shadow-lg shadow-blue-500/20">
          S
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-bold text-lg tracking-tight text-white">Siyantech Gym OS</span>
            <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
              PROD
            </span>
          </div>
          <div className="text-xs text-slate-400">
            Branch: <strong className="text-white">Jubilee Hills Flagship</strong>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav className="flex items-center bg-slate-900/90 p-1 rounded-xl border border-slate-800 text-xs font-semibold">
        <Link
          href="/desk"
          className={`px-4 py-2 rounded-lg flex items-center gap-2 transition ${
            pathname === '/desk'
              ? 'bg-blue-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <MonitorPlay className="w-4 h-4" />
          Front Desk Terminal
        </Link>
        <Link
          href="/dashboard"
          className={`px-4 py-2 rounded-lg flex items-center gap-2 transition ${
            pathname === '/dashboard'
              ? 'bg-blue-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <LayoutDashboard className="w-4 h-4" />
          Owner Cockpit & AI
        </Link>
      </nav>

      <!-- Quick Actions -->
      <div className="flex items-center gap-3">
        {onOpenOnboard && (
          <button
            onClick={onOpenOnboard}
            className="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-md shadow-blue-600/30 active:scale-95 transition"
          >
            + New Member (F2)
          </button>
        )}
        {onOpenShift && (
          <button
            onClick={onOpenShift}
            className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 active:scale-95 transition"
          >
            Shift Audit (F8)
          </button>
        )}
      </div>
    </header>
  );
}
