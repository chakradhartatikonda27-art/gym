'use client';

import React, { useState, useEffect } from 'react';

export default function DynamicQR() {
  const [seconds, setSeconds] = useState(15);
  const [rotation, setRotation] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds((prev) => {
        if (prev <= 1) {
          setRotation((r) => r + 90);
          return 15;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="glass-card p-6 rounded-2xl flex flex-col items-center text-center relative overflow-hidden">
      <div className="absolute top-4 left-4 flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-wider">
        <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        Dynamic Reception Kiosk
      </div>

      <div className="mt-6 mb-4 p-5 bg-white rounded-3xl shadow-2xl relative border-4 border-blue-500/30">
        <svg className="w-48 h-48" viewBox="0 0 100 100" fill="none">
          <rect width="100" height="100" fill="white" />
          {/* Eyes */}
          <rect x="6" y="6" width="24" height="24" fill="#0f172a" rx="4" />
          <rect x="10" y="10" width="16" height="16" fill="white" rx="2" />
          <rect x="14" y="14" width="8" height="8" fill="#2563eb" rx="1" />

          <rect x="70" y="6" width="24" height="24" fill="#0f172a" rx="4" />
          <rect x="74" y="10" width="16" height="16" fill="white" rx="2" />
          <rect x="78" y="14" width="8" height="8" fill="#2563eb" rx="1" />

          <rect x="6" y="70" width="24" height="24" fill="#0f172a" rx="4" />
          <rect x="10" y="74" width="16" height="16" fill="white" rx="2" />
          <rect x="14" y="78" width="8" height="8" fill="#2563eb" rx="1" />

          {/* Cryptographic Jitter Grid */}
          <g style={{ transform: `rotate(${rotation}deg)`, transformOrigin: '50px 50px' }}>
            <rect x="36" y="10" width="6" height="6" fill="#1e293b" />
            <rect x="46" y="16" width="8" height="6" fill="#1e293b" />
            <rect x="58" y="10" width="6" height="8" fill="#1e293b" />
            <rect x="36" y="24" width="8" height="8" fill="#2563eb" />
            <rect x="48" y="26" width="6" height="6" fill="#1e293b" />
            <rect x="36" y="38" width="12" height="6" fill="#1e293b" />
            <rect x="52" y="38" width="8" height="8" fill="#1e293b" />
            <rect x="66" y="38" width="10" height="6" fill="#1e293b" />
            <rect x="12" y="42" width="8" height="8" fill="#1e293b" />
            <rect x="24" y="46" width="6" height="8" fill="#1e293b" />
            <rect x="40" y="52" width="10" height="10" fill="#0f172a" />
            <rect x="55" y="52" width="8" height="6" fill="#1e293b" />
            <rect x="68" y="52" width="8" height="8" fill="#2563eb" />
            <rect x="36" y="68" width="8" height="8" fill="#1e293b" />
            <rect x="48" y="72" width="12" height="6" fill="#1e293b" />
            <rect x="64" y="68" width="10" height="10" fill="#1e293b" />
            <rect x="78" y="72" width="8" height="8" fill="#1e293b" />
          </g>
        </svg>
      </div>

      <div className="flex items-center gap-2 text-xs text-slate-400">
        <span>Rotating Token in:</span>
        <span className="font-mono font-bold text-white bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700">
          {seconds}s
        </span>
        <span className="text-blue-400 font-medium">(Anti-Screenshot HMAC)</span>
      </div>
    </div>
  );
}
