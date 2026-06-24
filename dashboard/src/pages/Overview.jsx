import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { TopBar }  from '../components/TopBar'
import { KpiCard } from '../components/KpiCard'
import { RiskBadge } from '../components/Badge'
import { useReportContext } from '../context/ReportContext'
import { computeStats, topRiskyFiles } from '../utils/parseReport'
import {
  RISK_COLORS, QUANTUM_COLORS,
  RISK_ORDER, QUANTUM_ORDER,
  RISK_LABELS, QUANTUM_LABELS,
  LANGUAGES, CATEGORIES,
} from '../utils/colors'

const TOOLTIP_STYLE = {
  contentStyle: { backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: 8, fontSize: 12 },
  labelStyle:   { color: '#f1f5f9' },
  itemStyle:    { color: '#94a3b8' },
}

export function Overview() {
  const { report }  = useReportContext()
  const navigate    = useNavigate()

  if (!report) return null

  const { findings } = report
  const stats    = computeStats(findings)
  const topFiles = topRiskyFiles(findings)
  const total    = stats.total

  // Quantum exposure gauge segments
  const quantumSegments = QUANTUM_ORDER.map(k => ({
    key:   k,
    count: stats.byQuantum[k] || 0,
    pct:   total > 0 ? Math.round((stats.byQuantum[k] || 0) / total * 100) : 0,
    color: QUANTUM_COLORS[k],
    label: QUANTUM_LABELS[k],
  }))

  const scoreColor =
    stats.quantumScore >= 70 ? '#ef4444' :
    stats.quantumScore >= 40 ? '#f97316' :
    '#22c55e'

  // Donut - by risk level
  const riskDonut = RISK_ORDER
    .filter(k => stats.byRisk[k])
    .map(k => ({ name: RISK_LABELS[k], value: stats.byRisk[k], color: RISK_COLORS[k] }))

  // Stacked bar - by language
  const langData = LANGUAGES.map(lang => {
    const lf   = findings.filter(f => f.language === lang)
    const entry = { lang }
    RISK_ORDER.forEach(r => { entry[r] = lf.filter(f => f.riskLevel === r).length })
    return entry
  }).filter(e => RISK_ORDER.some(r => e[r] > 0))

  // Bar - by category, colored by dominant quantum impact
  const catData = CATEGORIES.map(cat => {
    const cf      = findings.filter(f => f.category === cat)
    const counts  = {}
    cf.forEach(f => { counts[f.quantumImpact] = (counts[f.quantumImpact] || 0) + 1 })
    const dominant = QUANTUM_ORDER.find(q => counts[q]) || 'quantum_safe'
    return { cat, count: cf.length, color: QUANTUM_COLORS[dominant] }
  }).filter(e => e.count > 0)

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <TopBar title="Overview" />

      <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-5">

        {/* KPI row */}
        <div className="grid grid-cols-6 gap-3">
          <KpiCard label="Total Findings"  value={total} />
          <KpiCard label="Critical"        value={stats.byRisk.critical  || 0} color="#ef4444" />
          <KpiCard label="High"            value={stats.byRisk.high      || 0} color="#f97316" />
          <KpiCard label="Shor-Breakable"  value={stats.byQuantum.shor_breakable  || 0} color="#ef4444" />
          <KpiCard label="Already Weak"    value={stats.byQuantum.already_weak    || 0} color="#eab308" />
          <KpiCard label="Quantum-Safe"    value={stats.byQuantum.quantum_safe    || 0} color="#22c55e" />
        </div>

        {/* Quantum Exposure Gauge */}
        <div className="rounded-lg p-5" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-semibold text-slate-200">Quantum Exposure</span>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Quantum Risk Score</span>
              <span className="text-2xl font-bold" style={{ color: scoreColor }}>
                {stats.quantumScore}
              </span>
              <span className="text-xs text-slate-500">/ 100</span>
            </div>
          </div>

          {/* Gauge bar */}
          <div className="flex rounded-full overflow-hidden h-4">
            {quantumSegments.map(s =>
              s.pct > 0 && (
                <div
                  key={s.key}
                  style={{ width: `${s.pct}%`, backgroundColor: s.color }}
                  title={`${s.label}: ${s.count} (${s.pct}%)`}
                />
              )
            )}
          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-5 mt-3">
            {quantumSegments.map(s => (
              <div key={s.key} className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: s.color }} />
                <span className="text-xs text-slate-400">{s.label}</span>
                <span className="text-xs font-semibold" style={{ color: s.color }}>{s.pct}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-3 gap-4">
          {/* Donut - risk level */}
          <div className="rounded-lg p-4" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">By Risk Level</p>
            <ResponsiveContainer width="100%" height={190}>
              <PieChart>
                <Pie data={riskDonut} dataKey="value" nameKey="name" innerRadius={52} outerRadius={78} paddingAngle={2}>
                  {riskDonut.map(e => <Cell key={e.name} fill={e.color} />)}
                </Pie>
                <text x="50%" y="48%" textAnchor="middle" dominantBaseline="central" fill="#f1f5f9" fontSize={26} fontWeight="bold">{total}</text>
                <text x="50%" y="60%" textAnchor="middle" dominantBaseline="central" fill="#64748b" fontSize={11}>findings</text>
                <Tooltip {...TOOLTIP_STYLE} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Stacked bar - language */}
          <div className="rounded-lg p-4" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">By Language</p>
            <ResponsiveContainer width="100%" height={190}>
              <BarChart data={langData} barSize={30}>
                <XAxis dataKey="lang" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} width={24} />
                <Tooltip {...TOOLTIP_STYLE} />
                {RISK_ORDER.map(r => (
                  <Bar key={r} dataKey={r} name={RISK_LABELS[r]} stackId="a" fill={RISK_COLORS[r]} />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Bar - category */}
          <div className="rounded-lg p-4" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">By Category</p>
            <ResponsiveContainer width="100%" height={190}>
              <BarChart data={catData} barSize={22}>
                <XAxis dataKey="cat" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} width={24} />
                <Tooltip {...TOOLTIP_STYLE} />
                <Bar dataKey="count" name="Findings" radius={[4, 4, 0, 0]}>
                  {catData.map((e, i) => <Cell key={i} fill={e.color} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top risky files */}
        <div className="rounded-lg" style={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}>
          <div className="px-5 py-3" style={{ borderBottom: '1px solid #334155' }}>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Highest Risk Files</p>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr style={{ borderBottom: '1px solid #334155' }}>
                {['File', 'Critical', 'High', 'Medium', 'Total', 'Max Risk'].map(h => (
                  <th key={h} className="px-5 py-2 text-left text-xs text-slate-500 font-medium uppercase tracking-wider">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {topFiles.length === 0 ? (
                <tr><td colSpan={6} className="px-5 py-6 text-slate-500 text-center text-sm">No findings.</td></tr>
              ) : topFiles.map((f, i) => (
                <tr
                  key={i}
                  className="cursor-pointer transition-colors"
                  style={{ borderBottom: '1px solid #0f172a' }}
                  onClick={() => navigate('/filemap', { state: { selectedFile: f.file } })}
                  onMouseEnter={e => e.currentTarget.style.backgroundColor = '#334155'}
                  onMouseLeave={e => e.currentTarget.style.backgroundColor = ''}
                >
                  <td className="px-5 py-2.5 font-mono text-xs text-slate-300 max-w-xs truncate">{f.file}</td>
                  <td className="px-5 py-2.5 font-semibold" style={{ color: f.critical ? '#ef4444' : '#334155' }}>{f.critical}</td>
                  <td className="px-5 py-2.5 font-semibold" style={{ color: f.high    ? '#f97316' : '#334155' }}>{f.high}</td>
                  <td className="px-5 py-2.5 font-semibold" style={{ color: f.medium  ? '#eab308' : '#334155' }}>{f.medium}</td>
                  <td className="px-5 py-2.5 text-slate-300">{f.total}</td>
                  <td className="px-5 py-2.5"><RiskBadge level={f.maxRisk} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  )
}
