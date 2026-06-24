import React from 'react'
import { RISK_COLORS, QUANTUM_COLORS, RISK_LABELS, QUANTUM_LABELS } from '../utils/colors'

export function RiskBadge({ level }) {
  const color = RISK_COLORS[level] || '#6b7280'
  return (
    <span
      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold whitespace-nowrap"
      style={{ backgroundColor: color + '22', color, border: `1px solid ${color}55` }}
    >
      {RISK_LABELS[level] || level}
    </span>
  )
}

export function QuantumBadge({ impact }) {
  const color = QUANTUM_COLORS[impact] || '#6b7280'
  return (
    <span
      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold whitespace-nowrap"
      style={{ backgroundColor: color + '22', color, border: `1px solid ${color}55` }}
    >
      {QUANTUM_LABELS[impact] || impact}
    </span>
  )
}
