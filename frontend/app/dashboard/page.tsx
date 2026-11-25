'use client';

import React, { useState } from 'react';
import Navbar from '@/components/Navbar';
import { playTone } from '@/lib/audio';

export default function DashboardPage() {
  const [retentionMembers, setRetentionMembers] = useState([
    {
      id: '1',
      name: 'Rajesh Khanna',
      plan: 'Annual Strength',
      lastVisit: '11 Nov 2026',
      absenceDays: 11,
      trainer: 'Vikram Trainer',
      risk: 'High (42%)',
      sent: false,
    },
    {
      id: '2',
      name: 'Meera Sen',
      plan: '6-Month Fitness',
      lastVisit: '10 Nov 2026',
      absenceDays: 12,
      trainer: 'Anita Trainer',
      risk: 'Critical (21%)',
      sent: false,
    },
    {
      id: '3',
      name: 'Dinesh Karthik',
      plan: 'Quarterly Pro',
      lastVisit: '08 Nov 2026',
      absenceDays: 14,
      trainer: 'Unassigned',
      risk: 'Critical (15%)',
      sent: false,
    },
  ]);

  const handleSendPing = (id: string, name: string) => {
    playTone('success');
    setRetentionMembers((prev) =>
      prev.map((m) => (m.id === id ? { ...m, sent: true } : m))
    );
    alert(`Personalized reactivation offer sent to ${name} via WhatsApp Cloud API.`);
  };

  const handleSendAll = () => {
    playTone('success');
    setRetentionMembers((prev) => prev.map((m) => ({ ...m, sent: true })));
    alert('Automated retention workflow triggered for all 18 inactive members.');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">Owner Executive Cockpit</h1>
            <p className="text-xs text-slate-400">
              Real-time business profitability, cash audit reconciliation, and dropout prevention.
            </p>
          </div>
          <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold border border-blue-500/20 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-blue-400" /> AI Retention Engine: Active
          </span>
        </div>

        {/* Financial KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="glass-card p-5 rounded-2xl">
            <div className="text-xs text-slate-400">Monthly Revenue (MTD)</div>
            <div className="text-2xl font-extrabold text-white font-mono mt-1">₹4,85,000</div>
            <div className="text-xs text-emerald-400 mt-2 flex items-center gap-1">
              <span>↑ 14.2%</span> vs last month
            </div>
          </div>
          <div className="glass-card p-5 rounded-2xl">
            <div className="text-xs text-slate-400">Monthly Operating Expenses</div>
            <div className="text-2xl font-extrabold text-slate-300 font-mono mt-1">₹1,65,000</div>
            <div className="text-xs text-slate-400 mt-2">Rent, Staff, Power, Maintenance</div>
          </div>
          <div className="glass-card p-5 rounded-2xl border-emerald-500/30">
            <div className="text-xs text-emerald-400 font-semibold">Net Operating Surplus</div>
            <div className="text-2xl font-extrabold text-emerald-400 font-mono mt-1">₹3,20,000</div>
            <div className="text-xs text-slate-400 mt-2">Gross Margin: 65.9%</div>
          </div>
          <div className="glass-card p-5 rounded-2xl border-amber-500/30">
            <div className="text-xs text-amber-400 font-semibold">At-Risk Member Dropout</div>
            <div className="text-2xl font-extrabold text-amber-400 font-mono mt-1">18 Members</div>
            <div className="text-xs text-slate-400 mt-2">Absent &gt; 10 consecutive days</div>
          </div>
        </div>

        {/* Smart Retention Engine Table */}
        <div className="glass-card p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <span>🎯</span> Smart Retention Engine – Inactivity Follow-up Hub
              </h2>
              <p className="text-xs text-slate-400">
                AI automatically detects members who stopped coming and triggers personalized reactivation offers.
              </p>
            </div>
            <button
              onClick={handleSendAll}
              className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold active:scale-95 transition"
            >
              Send All Automated Pings
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800 bg-slate-900/40">
                <tr>
                  <th className="p-3">Member Name</th>
                  <th className="p-3">Active Plan</th>
                  <th className="p-3">Last Visit</th>
                  <th className="p-3">Absence</th>
                  <th className="p-3">Assigned Trainer</th>
                  <th className="p-3">Retention Probability</th>
                  <th className="p-3 text-right">One-Click Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {retentionMembers.map((m) => (
                  <tr
                    key={m.id}
                    className={`hover:bg-slate-900/40 transition ${
                      m.sent ? 'opacity-40' : ''
                    }`}
                  >
                    <td className="p-3 font-bold text-white">{m.name}</td>
                    <td className="p-3 text-slate-300">{m.plan}</td>
                    <td className="p-3 text-slate-400 font-mono">{m.lastVisit}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded bg-red-500/20 text-red-400 font-bold">
                        {m.absenceDays} Days
                      </span>
                    </td>
                    <td className="p-3 text-slate-300">{m.trainer}</td>
                    <td className="p-3">
                      <span className="text-amber-400 font-semibold">{m.risk}</span>
                    </td>
                    <td className="p-3 text-right">
                      <button
                        disabled={m.sent}
                        onClick={() => handleSendPing(m.id, m.name)}
                        className={`px-3 py-1 rounded-lg font-semibold transition ${
                          m.sent
                            ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                            : 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95'
                        }`}
                      >
                        {m.sent ? 'WhatsApp Sent ✔' : 'WhatsApp Retention Offer'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
