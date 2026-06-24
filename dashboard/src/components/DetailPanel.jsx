import React from 'react'
import { X } from 'lucide-react'
import { RiskBadge, QuantumBadge } from './Badge'
import { QUANTUM_COLORS } from '../utils/colors'

const MIGRATION_NOTES = {
  shor_breakable:
    'This algorithm is theoretically broken by Shor\'s algorithm on a cryptographically relevant quantum computer. Migrate to ML-KEM or ML-DSA (NIST FIPS 203/204).',
  grover_weakened:
    'Grover\'s algorithm halves the effective key size. Ensure key length ≥ 256 bits.',
  already_weak:
    'This algorithm is considered weak even without quantum threats. Replace immediately.',
  quantum_safe:
    'This algorithm is quantum-resistant per current NIST guidance.',
}

function Row({ label, value, mono = false }) {
  return (
    <div>
      <p className="text-xs text-slate-500 uppercase tracking-wider mb-0.5">{label}</p>
      <p className={`text-sm text-slate-200 ${mono ? 'font-mono break-all' : ''}`}>{value}</p>
    </div>
  )
}

export function DetailPanel({ finding, onClose }) {
  if (!finding) return null

  const migrationColor = QUANTUM_COLORS[finding.quantumImpact] || '#6b7280'

  return (
    <div
      className="flex flex-col h-full overflow-y-auto flex-shrink-0"
      style={{ width: 400, borderLeft: '1px solid #334155', backgroundColor: '#1e293b' }}
    >
      {/* Header */}
      <div
        className="flex items-start justify-between p-5 flex-shrink-0"
        style={{ borderBottom: '1px solid #334155' }}
      >
        <div className="flex flex-col gap-2 mr-3">
          <span className="text-lg font-bold text-white leading-tight">{finding.algorithm}</span>
          <div className="flex flex-wrap gap-2">
            <RiskBadge level={finding.riskLevel} />
            <QuantumBadge impact={finding.quantumImpact} />
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-slate-500 hover:text-white transition-colors flex-shrink-0 p-1"
        >
          <X size={16} />
        </button>
      </div>

      {/* Body */}
      <div className="flex flex-col gap-5 p-5">
        <Row label="Rule ID" value={finding.id || '-'} />
        {finding.oid && <Row label="OID" value={finding.oid} mono />}
        <Row label="Category" value={finding.category} />
        <Row label="Language" value={finding.language} />

        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-0.5">Location</p>
          <p className="text-sm text-slate-200 font-mono break-all">{finding.file}</p>
          <p className="text-xs text-slate-500 mt-0.5">Line {finding.line}</p>
        </div>

        {finding.snippet && (
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Snippet</p>
            <pre
              className="p-3 rounded-lg text-xs text-green-300 overflow-x-auto leading-relaxed"
              style={{ backgroundColor: '#0f172a', fontFamily: 'ui-monospace, monospace' }}
            >
              {finding.snippet}
            </pre>
          </div>
        )}

        {finding.notes && (
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-0.5">Notes</p>
            <p className="text-sm text-slate-300 leading-relaxed">{finding.notes}</p>
          </div>
        )}

        {/* Migration guidance */}
        <div
          className="p-4 rounded-lg"
          style={{
            backgroundColor: migrationColor + '11',
            border: `1px solid ${migrationColor}33`,
          }}
        >
          <p
            className="text-xs font-semibold uppercase tracking-wider mb-2"
            style={{ color: migrationColor }}
          >
            Migration Guidance
          </p>
          <p className="text-xs leading-relaxed" style={{ color: migrationColor + 'cc' }}>
            {MIGRATION_NOTES[finding.quantumImpact] || '-'}
          </p>
        </div>
      </div>
    </div>
  )
}
