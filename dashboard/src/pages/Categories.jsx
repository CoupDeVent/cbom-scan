import React, { useState } from 'react'
import {
  PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { TopBar }   from '../components/TopBar'
import { KpiCard }  from '../components/KpiCard'
import { RiskBadge, QuantumBadge } from '../components/Badge'
import { DetailPanel } from '../components/DetailPanel'
import { useReportContext } from '../context/ReportContext'
import {
  RISK_COLORS, QUANTUM_COLORS,
  QUANTUM_ORDER, QUANTUM_LABELS,
  CATEGORIES,
} from '../utils/colors'

const TOOLTIP_STYLE = {
  contentStyle: { backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: 8, fontSize: 12 },
  labelStyle:   { color: '#f1f5f9' },
  itemStyle:    { color: '#94a3b8' },
}

export function Categories() {
  const { report }  = useReportContext()
  const [tab,      setTab]      = useState('symmetric')
  const [selected, setSelected] = useState(null)

  if (!report) return null

  const catFindings = report.findings.filter(f => f.category === tab)
  const total    = catFindings.length
  const critical = catFindings.filter(f => f.riskLevel      === 'critical').length
  const shor     = catFindings.filter(f => f.quantumImpact  === 'shor_breakable').length
  const safe     = catFindings.filter(f => f.quantumImpact  === 'quantum_safe').length

  // Donut - quantum impact distribution within this category
  const quantumDonut = QUANTUM_ORDER
    .map(k => ({
      name:  QUANTUM_LABELS[k],
      value: catFindings.filter(f => f.quantumImpact === k).length,
      color: QUANTUM_COLORS[k],
    }))
    .filter(e => e.value > 0)

  // Horizontal bar - top 5 algorithms by finding count
  const algoCounts = {}
  catFindings.forEach(f => { algoCounts[f.algorithm] = (algoCounts[f.algorithm] || 0) + 1 })
  const topAlgos = Object.entries(algoCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name, count]) => ({ name, count }))

  return (
    <div className="flex flex-1 overflow-hidden">
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopBar title="Categories" />

        {/* Tab bar */}
        <div
          className="flex gap-1 px-6 py-3 flex-shrink-0"
          style={{ borderBottom: '1px solid #334155', backgroundColor: '#1e293b' }}
        >
          {CATEGORIES.map(t => {
            const count = report.findings.filter(f => f.category === t).length
            const active = tab === t
            return (
              <button
                key={t}
                onClick={() => { setTab(t); setSelected(null) }}
                className="flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-medium transition-colors"
                style={{
                  backgroundColor: active ? '#312e81' : 'transparent',
                  color:           active ? '#a5b4fc' : '#64748b',
                  border:          active ? '1px solid #4338ca' : '1px solid transparent',
                }}
              >
                {t}
                <span
                  className="text-xs rounded-full px-1.5 py-0"
                  style={{ backgroundColor: active ? '#4338ca' : '#334155', color: active ? '#c7d2fe' : '#94a3b8' }}
                >
                  {count}
                </span>
              </button>
            )
          })}
        </div>

        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-5">

          {/* KPI row */}
          <div className="grid grid-cols-4 gap-3">
            <KpiCard label="Total in Category" value={total} />
            <KpiCard label="Critical"           value={critical} color="#ef4444" />
            <KpiCard label="Shor-Breakable"     value={shor}     color="#ef4444" />
            <KpiCard label="Quantum-Safe"       value={safe}     color="#22c55e" />
          </div>

          {/* Charts */}
          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg p-4" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
                By Quantum Impact
              </p>
              {quantumDonut.length > 0 ? (
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={quantumDonut}
                      dataKey="value"
                      nameKey="name"
                      innerRadius={52}
                      outerRadius={78}
                      paddingAngle={2}
                    >
                      {quantumDonut.map(e => <Cell key={e.name} fill={e.color} />)}
                    </Pie>
                    <Tooltip {...TOOLTIP_STYLE} />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-48 text-slate-600 text-sm">
                  No data for this category.
                </div>
              )}
            </div>

            <div className="rounded-lg p-4" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
                Top Algorithms
              </p>
              {topAlgos.length > 0 ? (
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={topAlgos} layout="vertical" barSize={16}>
                    <XAxis
                      type="number"
                      tick={{ fill: '#64748b', fontSize: 11 }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      type="category"
                      dataKey="name"
                      tick={{ fill: '#94a3b8', fontSize: 11 }}
                      axisLine={false}
                      tickLine={false}
                      width={90}
                    />
                    <Tooltip {...TOOLTIP_STYLE} />
                    <Bar dataKey="count" name="Findings" fill="#6366f1" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-48 text-slate-600 text-sm">
                  No data for this category.
                </div>
              )}
            </div>
          </div>

          {/* Findings mini-table */}
          <div className="rounded-lg" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
            <div className="px-5 py-3" style={{ borderBottom: '1px solid #334155' }}>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Findings - {tab}
              </p>
            </div>

            {catFindings.length === 0 ? (
              <p className="px-5 py-6 text-sm text-slate-600 text-center">
                No findings in this category.
              </p>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr style={{ borderBottom: '1px solid #334155' }}>
                    {['Rule ID', 'Algorithm', 'Quantum Impact', 'Risk Level', 'File', 'Line'].map(h => (
                      <th
                        key={h}
                        className="px-5 py-2 text-left text-xs text-slate-500 font-medium uppercase tracking-wider"
                      >
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {catFindings.map(f => (
                    <tr
                      key={f.uid}
                      onClick={() => setSelected(f)}
                      className="cursor-pointer transition-colors"
                      style={{
                        borderBottom: '1px solid #0f172a',
                        borderLeft:   `3px solid ${RISK_COLORS[f.riskLevel] || '#334155'}`,
                      }}
                      onMouseEnter={e => e.currentTarget.style.backgroundColor = '#334155'}
                      onMouseLeave={e => e.currentTarget.style.backgroundColor = ''}
                    >
                      <td className="px-5 py-2.5 font-mono text-xs text-slate-500">{f.id}</td>
                      <td className="px-5 py-2.5 text-slate-200 font-medium">{f.algorithm}</td>
                      <td className="px-5 py-2.5"><QuantumBadge impact={f.quantumImpact} /></td>
                      <td className="px-5 py-2.5"><RiskBadge    level={f.riskLevel} /></td>
                      <td className="px-5 py-2.5 font-mono text-xs text-slate-400 max-w-xs">
                        <span className="truncate block max-w-xs" title={f.file}>{f.file}</span>
                      </td>
                      <td className="px-5 py-2.5 text-slate-500 text-xs">{f.line}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

        </div>
      </div>

      {selected && <DetailPanel finding={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
