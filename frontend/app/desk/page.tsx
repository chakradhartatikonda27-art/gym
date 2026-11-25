'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import DynamicQR from '@/components/DynamicQR';
import OnboardModal from '@/components/OnboardModal';
import ShiftModal from '@/components/ShiftModal';
import { playTone } from '@/lib/audio';

interface FeedItem {
  id: string;
  name: string;
  memberCode: string;
  plan: string;
  status: 'ALLOWED' | 'WARNING_DUES' | 'DENIED_EXPIRED';
  time: string;
  dues?: number;
}

export default function DeskPage() {
  const [isOnboardOpen, setIsOnboardOpen] = useState(false);
  const [isShiftOpen, setIsShiftOpen] = useState(false);
  const [headcount, setHeadcount] = useState(42);
  const [checkins, setCheckins] = useState(118);
  const [cashDrawer, setCashDrawer] = useState(14500);
  const [upiTotal, setUpiTotal] = useState(28000);

  const [feed, setFeed] = useState<FeedItem[]>([
    {
      id: '1',
      name: 'Rahul Verma',
      memberCode: 'GYM-1024',
      plan: 'Annual Strength & Cardio • 142 Days Left',
      status: 'ALLOWED',
      time: '07:42 AM',
    },
    {
      id: '2',
      name: 'Sneha Reddy',
      memberCode: 'GYM-1098',
      plan: '3-Month Fitness • ₹1,500 Balance Due',
      status: 'WARNING_DUES',
      dues: 1500,
      time: '07:40 AM',
    },
    {
      id: '3',
      name: 'Vikram Joshi',
      memberCode: 'GYM-0842',
      plan: 'Monthly Starter • Expired Yesterday',
      status: 'DENIED_EXPIRED',
      time: '07:38 AM',
    },
  ]);

  // Keyboard shortcut listener (F2, F8)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'F2') {
        e.preventDefault();
        setIsOnboardOpen(true);
      }
      if (e.key === 'F8') {
        e.preventDefault();
        setIsShiftOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSimulate = (type: 'active' | 'dues' | 'expired') => {
    const now = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
    if (type === 'active') {
      playTone('success');
      setHeadcount((h) => h + 1);
      setCheckins((c) => c + 1);
      setFeed((prev) => [
        {
          id: Date.now().toString(),
          name: 'Arjun Kapoor',
          memberCode: `GYM-${Math.floor(1000 + Math.random() * 9000)}`,
          plan: 'Annual Strength & Cardio • 365 Days Left',
          status: 'ALLOWED',
          time: now,
        },
        ...prev,
      ]);
    } else if (type === 'dues') {
      playTone('warning');
      setFeed((prev) => [
        {
          id: Date.now().toString(),
          name: 'Kiran Patel',
          memberCode: 'GYM-2210',
          plan: 'Quarterly Pro • ₹2,000 Overdue Balance',
          status: 'WARNING_DUES',
          dues: 2000,
          time: now,
        },
        ...prev,
      ]);
    } else {
      playTone('danger');
      setFeed((prev) => [
        {
          id: Date.now().toString(),
          name: 'Manish Sharma',
          memberCode: 'GYM-0711',
          plan: 'Monthly Starter • Plan Expired (Access Denied)',
          status: 'DENIED_EXPIRED',
          time: now,
        },
        ...prev,
      ]);
    }
  };

  const handleCollectDue = (name: string, amount: number) => {
    playTone('success');
    setUpiTotal((u) => u + amount);
    alert(`₹${amount} collected from ${name} via UPI. Ledger reconciled.`);
  };

  const handleOnboardSuccess = (member: { name: string; amount: number }) => {
    setFeed((prev) => [
      {
        id: Date.now().toString(),
        name: member.name,
        memberCode: `GYM-${Math.floor(1000 + Math.random() * 9000)}`,
        plan: 'Annual Strength & Cardio • 365 Days Left',
        status: 'ALLOWED',
        time: 'Just now',
      },
      ...prev,
    ]);
    setCashDrawer((c) => c + 5000);
    setUpiTotal((u) => u + (member.amount - 5000));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar
        onOpenOnboard={() => setIsOnboardOpen(true)}
        onOpenShift={() => setIsShiftOpen(true)}
      />

      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        {/* KPI Strip */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="glass-card p-4 rounded-2xl">
            <div className="text-xs text-slate-400 font-medium">Inside Gym Now</div>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-emerald-400 font-mono">{headcount}</span>
              <span className="text-xs text-slate-500">/ 150 Cap</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
              <div className="bg-emerald-500 h-full rounded-full transition-all" style={{ width: `${(headcount / 150) * 100}%` }} />
            </div>
          </div>

          <div className="glass-card p-4 rounded-2xl">
            <div className="text-xs text-slate-400 font-medium">Today's Check-ins</div>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-white font-mono">{checkins}</span>
              <span className="text-xs text-emerald-400 font-semibold">↑ 18% peak</span>
            </div>
            <div className="text-[11px] text-slate-400 mt-2">Zero bottlenecks recorded</div>
          </div>

          <div className="glass-card p-4 rounded-2xl">
            <div className="text-xs text-slate-400 font-medium">Cash in Drawer (Shift)</div>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-white font-mono">₹{cashDrawer.toLocaleString('en-IN')}</span>
            </div>
            <div className="text-[11px] text-slate-400 mt-2">Opening Float: ₹2,000</div>
          </div>

          <div className="glass-card p-4 rounded-2xl">
            <div className="text-xs text-slate-400 font-medium">Digital UPI Collections</div>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-blue-400 font-mono">₹{upiTotal.toLocaleString('en-IN')}</span>
            </div>
            <div className="text-[11px] text-slate-400 mt-2">Auto-reconciled in ledger</div>
          </div>
        </div>

        {/* Main Work Area */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Dynamic QR */}
          <div className="lg:col-span-5 space-y-4">
            <DynamicQR />

            <div className="glass-card p-4 rounded-2xl">
              <span className="text-xs font-bold text-slate-300 block mb-2 uppercase tracking-wider">
                Simulate Member Scans (Demo Cues):
              </span>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => handleSimulate('active')}
                  className="py-2 px-1 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold active:scale-95 transition"
                >
                  Valid Pass
                </button>
                <button
                  onClick={() => handleSimulate('dues')}
                  className="py-2 px-1 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-bold active:scale-95 transition"
                >
                  Pending Dues
                </button>
                <button
                  onClick={() => handleSimulate('expired')}
                  className="py-2 px-1 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-bold active:scale-95 transition"
                >
                  Expired Pass
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: Live Feed */}
          <div className="lg:col-span-7">
            <div className="glass-card p-6 rounded-2xl h-full flex flex-col">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
                <div className="flex items-center gap-2.5">
                  <span className="w-3 h-3 rounded-full bg-emerald-400" />
                  <span className="font-bold text-white text-sm">Live Verification Feed</span>
                  <span className="text-[10px] text-slate-500 font-mono bg-slate-900 px-2 py-0.5 rounded">&lt;150ms P95</span>
                </div>
                <span className="text-xs text-slate-400">Automated Audit Log</span>
              </div>

              <div className="space-y-3 overflow-y-auto max-h-[500px] pr-2">
                {feed.map((item) => (
                  <div
                    key={item.id}
                    className={`p-3.5 rounded-xl border flex items-center justify-between transition ${
                      item.status === 'ALLOWED'
                        ? 'bg-slate-900/80 border-emerald-500/30'
                        : item.status === 'WARNING_DUES'
                        ? 'bg-slate-900/80 border-amber-500/40'
                        : 'bg-slate-900/80 border-red-500/40'
                    }`}
                  >
                    <div>
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        {item.name}
                        <span className="text-[10px] text-slate-400 font-mono">{item.memberCode}</span>
                      </div>
                      <div className="text-xs text-slate-400 mt-0.5">{item.plan}</div>
                    </div>

                    <div className="text-right flex flex-col items-end gap-1">
                      {item.status === 'ALLOWED' && (
                        <span className="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          ACCESS ALLOWED
                        </span>
                      )}
                      {item.status === 'WARNING_DUES' && (
                        <>
                          <span className="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/30">
                            DUES WARNING
                          </span>
                          {item.dues && (
                            <button
                              onClick={() => handleCollectDue(item.name, item.dues!)}
                              className="text-xs px-2.5 py-1 bg-amber-600 hover:bg-amber-500 text-white rounded-lg font-semibold active:scale-95 transition"
                            >
                              Collect ₹{item.dues}
                            </button>
                          )}
                        </>
                      )}
                      {item.status === 'DENIED_EXPIRED' && (
                        <>
                          <span className="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-red-500/20 text-red-400 border border-red-500/30">
                            ACCESS DENIED
                          </span>
                          <button
                            onClick={() => setIsOnboardOpen(true)}
                            className="text-xs px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold active:scale-95 transition"
                          >
                            Renew Plan
                          </button>
                        </>
                      )}
                      <div className="text-[10px] text-slate-500 font-mono">{item.time}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>

      <OnboardModal
        isOpen={isOnboardOpen}
        onClose={() => setIsOnboardOpen(false)}
        onSuccess={handleOnboardSuccess}
      />

      <ShiftModal
        isOpen={isShiftOpen}
        onClose={() => setIsShiftOpen(false)}
        onSuccess={(varAmt) => {
          alert(`Shift closed with ${varAmt === 0 ? 'zero discrepancy' : `variance of ₹${varAmt}`}. Report dispatched.`);
        }}
      />
    </div>
  );
}
