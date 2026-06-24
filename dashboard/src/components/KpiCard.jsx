import React from 'react'

export function KpiCard({ label, value, color = '#f1f5f9' }) {
  return (
    <div
      className="rounded-lg p-4 flex flex-col gap-2"
      style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
    >
      <span className="text-xs text-slate-400 uppercase tracking-wider font-medium leading-none">
        {label}
      </span>
      <span className="text-3xl font-bold leading-none" style={{ color }}>
        {value}
      </span>
    </div>
  )
}
