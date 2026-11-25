'use client';

import React, { useState } from 'react';
import { X } from 'lucide-react';
import { playTone } from '@/lib/audio';

interface ShiftModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (discrepancy: number) => void;
}

export default function ShiftModal({ isOpen, onClose, onSuccess }: ShiftModalProps) {
  const [counted, setCounted] = useState<number>(18150);
  const expected = 18150;
  const variance = counted - expected;

  if (!isOpen) return null;

  const handleSubmit = () => {
    playTone('success');
    onSuccess(variance);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="glass-card border border-slate-700 rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl animate-in fade-in duration-200">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
          <div>
            <h3 className="text-base font-bold text-white">Shift Handover & Cash Audit</h3>
            <p className="text-xs text-slate-400">Shift #CR-418 • Receptionist: Priya Sharma</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4 text-xs">
          <div className="p-3.5 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5 font-mono">
            <div className="flex justify-between text-slate-400">
              <span>Opening Cash Float:</span>
              <span>₹ 2,000.00</span>
            </div>
            <div className="flex justify-between text-emerald-400">
              <span>(+) Cash Collected:</span>
              <span>₹ 16,500.00</span>
            </div>
            <div className="flex justify-between text-red-400">
              <span>(-) Petty Expenses (Water Cans):</span>
              <span>- ₹ 350.00</span>
            </div>
            <div className="flex justify-between font-bold text-white pt-2 border-t border-slate-800 text-sm">
              <span>Expected Cash in Drawer:</span>
              <span className="text-blue-400">₹ 18,150.00</span>
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1.5">
              Counted Physical Cash in Drawer *
            </label>
            <div className="flex gap-2">
              <span className="px-3 py-2 bg-slate-800 rounded-xl text-slate-400 font-mono">₹</span>
              <input
                type="number"
                value={counted}
                onChange={(e) => setCounted(parseFloat(e.target.value) || 0)}
                className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          {/* Dynamic Variance Box */}
          <div
            className={`p-3 rounded-xl border flex items-center justify-between font-mono ${
              variance === 0
                ? 'bg-emerald-500/10 border-emerald-500/30'
                : variance < 0
                ? 'bg-red-500/10 border-red-500/40 animate-pulse'
                : 'bg-blue-500/10 border-blue-500/30'
            }`}
          >
            <span className="text-slate-400">Variance / Difference:</span>
            <span
              className={`font-bold ${
                variance === 0
                  ? 'text-emerald-400'
                  : variance < 0
                  ? 'text-red-400'
                  : 'text-blue-400'
              }`}
            >
              {variance === 0
                ? '₹0.00 (Balanced Match)'
                : variance < 0
                ? `-₹${Math.abs(variance).toFixed(2)} (Cash Shortage Alert)`
                : `+₹${variance.toFixed(2)} (Surplus Cash)`}
            </span>
          </div>

          {variance < 0 && (
            <div>
              <label className="text-xs font-semibold text-red-400 block mb-1">
                Mandatory Shortage Reason (Sends WhatsApp Alert to Owner):
              </label>
              <textarea
                placeholder="Explain shortage for owner audit..."
                className="w-full bg-slate-900 border border-red-500/40 rounded-xl p-2.5 text-xs text-white focus:outline-none"
              />
            </div>
          )}

          <div className="pt-3 border-t border-slate-800 flex justify-end gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold shadow-lg transition"
            >
              Close Shift & Handover
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
