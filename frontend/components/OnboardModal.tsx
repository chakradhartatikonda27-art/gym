'use client';

import React, { useState } from 'react';
import { X, CheckCircle2 } from 'lucide-react';
import { playTone } from '@/lib/audio';

interface OnboardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (member: { name: string; phone: string; plan: string; amount: number }) => void;
}

export default function OnboardModal({ isOpen, onClose, onSuccess }: OnboardModalProps) {
  const [phone, setPhone] = useState('+91 98490 12345');
  const [name, setName] = useState('Arjun Kapoor');
  const [planValue, setPlanValue] = useState('14999');
  const [cash, setCash] = useState('5000');
  const [upi, setUpi] = useState('9999');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    playTone('success');
    onSuccess({
      name,
      phone,
      plan: 'Annual Strength & Cardio',
      amount: parseInt(planValue, 10),
    });
    onClose();
  };

  const basePrice = (parseFloat(planValue) / 1.18).toFixed(2);
  const taxPrice = (parseFloat(planValue) - parseFloat(basePrice)).toFixed(2);

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="glass-card border border-slate-700 rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl animate-in fade-in duration-200">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              Fast Member Onboarding
              <span className="px-2 py-0.5 text-[10px] bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-full font-semibold">
                Under 45s
              </span>
            </h3>
            <p className="text-xs text-slate-400">Captures member, plan, split payment, and sends WhatsApp pass.</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Mobile Number *</label>
                <input
                  type="tel"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-mono focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Full Name *</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-xs font-semibold text-slate-300 block mb-1">Gender</label>
                  <select className="w-full bg-slate-900 border border-slate-700 rounded-xl px-2 py-2 text-xs text-white focus:outline-none">
                    <option>Male</option>
                    <option>Female</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-300 block mb-1">Emergency Phone</label>
                  <input
                    type="tel"
                    defaultValue="+91 98490 99999"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none"
                  />
                </div>
              </div>
              <div className="pt-1">
                <label className="flex items-center gap-2 text-xs text-slate-400 cursor-pointer">
                  <input type="checkbox" defaultChecked className="rounded bg-slate-900 border-slate-700 text-blue-600" />
                  <span>Signed liability & health waiver</span>
                </label>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Select Membership Plan *</label>
                <select
                  value={planValue}
                  onChange={(e) => setPlanValue(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
                >
                  <option value="14999">Annual Strength & Cardio - ₹14,999</option>
                  <option value="8999">Half-Yearly Fitness - ₹8,999</option>
                  <option value="4999">Quarterly Pro - ₹4,999</option>
                </select>
              </div>
              <div className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 text-xs space-y-1">
                <div className="flex justify-between text-slate-400">
                  <span>Base Price:</span>
                  <span>₹{basePrice}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>GST (18%):</span>
                  <span>₹{taxPrice}</span>
                </div>
                <div className="flex justify-between font-bold text-white pt-1 border-t border-slate-800">
                  <span>Total Amount:</span>
                  <span className="text-blue-400">₹{parseInt(planValue).toLocaleString('en-IN')}.00</span>
                </div>
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Payment Mode Split</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    value={cash}
                    onChange={(e) => setCash(e.target.value)}
                    placeholder="Cash ₹"
                    className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none"
                  />
                  <input
                    type="number"
                    value={upi}
                    onChange={(e) => setUpi(e.target.value)}
                    placeholder="UPI ₹"
                    className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none"
                  />
                </div>
              </div>
              <div className="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Automated WhatsApp welcome pass & QR queued
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-600/30 active:scale-95 transition"
            >
              Submit & Activate Member
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
