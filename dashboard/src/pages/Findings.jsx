import React, { useState, useMemo } from 'react'
import { X, Search, ChevronLeft, ChevronRight } from 'lucide-react'
import { TopBar }       from '../components/TopBar'
import { RiskBadge, QuantumBadge } from '../components/Badge'
import { DetailPanel }  from '../components/DetailPanel'
import { useReportContext } from '../context/ReportContext'
import { RISK_COLORS, RISK_ORDER } from '../utils/colors'

const PAGE_SIZE  = 25
const RISK_RANK  = Object.fromEntries(RISK_ORDER.map((r, i) => [r, i]))

function Select({ label, value, onChange, options }) {
  return (
    <select
      value={value}
      onChange={e => onChange(e.target.value)}
      className="text-sm rounded-lg px-3 py-1.5 text-slate-200 outline-none"
      style={{ backgroundColor: '#0f172a', border: '1px solid #334155' }}
    >
      <option value="">{label}</option>
      {options.map(o => <option key={o} value={o}>{o}</option>)}
    </select>
  )
}

function Chip({ label, onRemove }) {
  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium"
      style={{ backgroundColor: '#312e81', color: '#a5b4fc' }}
    >
      {label}
      <button onClick={onRemove} className="hover:text-white ml-0.5">
        <X size={10} />
      </button>
    </span>
  )
}

const COLS = [
  { key: 'id',           label: 'Rule ID' },
  { key: 'algorithm',    label: 'Algorithm' },
  { key: 'language',     label: 'Language' },
  { key: 'category',     label: 'Category' },
  { key: 'quantumImpact',label: 'Quantum Impact' },
  { key: 'riskLevel',    label: 'Risk Level' },
  { key: 'file',         label: 'File' },
  { key: 'line',         label: 'Line' },
]

export function Findings() {
  const { report } = useReportContext()
  const [selected, setSelected] = useState(null)
  const [page,     setPage]     = useState(1)
  const [sortKey,  setSortKey]  = useState('riskLevel')
  const [sortDir,  setSortDir]  = useState('asc')
  const [filters,  setFilters]  = useState({
    language: '', category: '', quantumImpact: '', riskLevel: '', search: '',
  })

  if (!report) return null

  const setFilter = (key, val) => { setFilters(f => ({ ...f, [key]: val })); setPage(1) }
  const clearFilter = (key)   => setFilter(key, '')
  const resetAll    = ()      => {
    setFilters({ language: '', category: '', quantumImpact: '', riskLevel: '', search: '' })
    setPage(1)
  }

  const filtered = useMemo(() => {
    let f = report.findings
    if (filters.language)     f = f.filter(x => x.language      === filters.language)
    if (filters.category)     f = f.filter(x => x.category      === filters.category)
    if (filters.quantumImpact)f = f.filter(x => x.quantumImpact === filters.quantumImpact)
    if (filters.riskLevel)    f = f.filter(x => x.riskLevel     === filters.riskLevel)
    if (filters.search) {
      const q = filters.search.toLowerCase()
      f = f.filter(x =>
        x.algorithm.toLowerCase().includes(q) ||
        x.file.toLowerCase().includes(q)      ||
        x.snippet.toLowerCase().includes(q)
      )
    }
    return [...f].sort((a, b) => {
      let va = a[sortKey], vb = b[sortKey]
      if (sortKey === 'riskLevel') { va = RISK_RANK[va] ?? 99; vb = RISK_RANK[vb] ?? 99 }
      if (sortKey === 'line')      { va = Number(va); vb = Number(vb) }
      const cmp = typeof va === 'number' ? va - vb : String(va).localeCompare(String(vb))
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [report.findings, filters, sortKey, sortDir])

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const paginated  = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  const handleSort = (key) => {
    if (sortKey === key) setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    else { setSortKey(key); setSortDir('asc') }
  }

  const activeChips = Object.entries(filters).filter(([k, v]) => v && k !== 'search')
  const hasFilters  = activeChips.length > 0 || filters.search

  return (
    <div className="flex flex-1 overflow-hidden">
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopBar title="Findings" />

        {/* Filter bar */}
        <div
          className="flex flex-wrap items-center gap-2 px-6 py-3 flex-shrink-0"
          style={{ borderBottom: '1px solid #334155', backgroundColor: '#1e293b' }}
        >
          <Select label="Language"       value={filters.language}      onChange={v => setFilter('language', v)}      options={['python','java','javascript']} />
          <Select label="Category"       value={filters.category}      onChange={v => setFilter('category', v)}      options={['symmetric','asymmetric','hash','mac','kdf','pqc']} />
          <Select label="Quantum Impact" value={filters.quantumImpact} onChange={v => setFilter('quantumImpact', v)} options={['shor_breakable','grover_weakened','already_weak','quantum_safe']} />
          <Select label="Risk Level"     value={filters.riskLevel}     onChange={v => setFilter('riskLevel', v)}     options={['critical','high','medium','low','info']} />

          <div
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
            style={{ backgroundColor: '#0f172a', border: '1px solid #334155' }}
          >
            <Search size={13} className="text-slate-500" />
            <input
              type="text"
              placeholder="Search algorithm, file, snippet…"
              value={filters.search}
              onChange={e => setFilter('search', e.target.value)}
              className="bg-transparent text-sm text-slate-200 outline-none w-52 placeholder-slate-600"
            />
            {filters.search && (
              <button onClick={() => setFilter('search', '')} className="text-slate-500 hover:text-white">
                <X size={12} />
              </button>
            )}
          </div>

          {hasFilters && (
            <button onClick={resetAll} className="text-xs text-indigo-400 hover:text-indigo-300 ml-1">
              Reset filters
            </button>
          )}

          <span className="ml-auto text-xs text-slate-500">{filtered.length} findings</span>
        </div>

        {/* Active filter chips */}
        {activeChips.length > 0 && (
          <div
            className="flex flex-wrap gap-2 px-6 py-2 flex-shrink-0"
            style={{ borderBottom: '1px solid #334155' }}
          >
            {activeChips.map(([k, v]) => (
              <Chip key={k} label={`${k}: ${v}`} onRemove={() => clearFilter(k)} />
            ))}
          </div>
        )}

        {/* Table */}
        <div className="flex-1 overflow-auto">
          {filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full gap-3 text-slate-500">
              <p className="text-sm">No findings match the current filters.</p>
              <button onClick={resetAll} className="text-sm text-indigo-400 hover:text-indigo-300">
                Reset filters
              </button>
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead className="sticky top-0 z-10" style={{ backgroundColor: '#0f172a' }}>
                <tr style={{ borderBottom: '1px solid #334155' }}>
                  {COLS.map(c => (
                    <th
                      key={c.key}
                      onClick={() => handleSort(c.key)}
                      className="px-4 py-2.5 text-left text-xs text-slate-500 font-medium uppercase tracking-wider cursor-pointer select-none whitespace-nowrap"
                      onMouseEnter={e => e.currentTarget.style.color = '#94a3b8'}
                      onMouseLeave={e => e.currentTarget.style.color = ''}
                    >
                      {c.label}
                      {sortKey === c.key && (
                        <span className="ml-1 text-indigo-400">{sortDir === 'asc' ? '↑' : '↓'}</span>
                      )}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {paginated.map(f => (
                  <tr
                    key={f.uid}
                    onClick={() => setSelected(f)}
                    className="cursor-pointer transition-colors"
                    style={{ borderBottom: '1px solid #1e293b', borderLeft: `3px solid ${RISK_COLORS[f.riskLevel] || '#334155'}` }}
                    onMouseEnter={e => e.currentTarget.style.backgroundColor = '#1e293b'}
                    onMouseLeave={e => e.currentTarget.style.backgroundColor = ''}
                  >
                    <td className="px-4 py-2.5 font-mono text-xs text-slate-500">{f.id}</td>
                    <td className="px-4 py-2.5 text-slate-200 font-medium">{f.algorithm}</td>
                    <td className="px-4 py-2.5 text-slate-400">{f.language}</td>
                    <td className="px-4 py-2.5 text-slate-400">{f.category}</td>
                    <td className="px-4 py-2.5"><QuantumBadge impact={f.quantumImpact} /></td>
                    <td className="px-4 py-2.5"><RiskBadge level={f.riskLevel} /></td>
                    <td className="px-4 py-2.5 font-mono text-xs text-slate-400 max-w-xs">
                      <span className="truncate block max-w-xs" title={f.file}>{f.file}</span>
                    </td>
                    <td className="px-4 py-2.5 text-slate-500 text-xs">{f.line}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div
            className="flex items-center justify-between px-6 py-3 flex-shrink-0"
            style={{ borderTop: '1px solid #334155', backgroundColor: '#1e293b' }}
          >
            <span className="text-xs text-slate-500">
              {filtered.length} findings · page {page} of {totalPages}
            </span>
            <div className="flex gap-2">
              <button
                disabled={page === 1}
                onClick={() => setPage(p => p - 1)}
                className="p-1.5 rounded text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                style={{ backgroundColor: '#334155' }}
              >
                <ChevronLeft size={13} />
              </button>
              <button
                disabled={page === totalPages}
                onClick={() => setPage(p => p + 1)}
                className="p-1.5 rounded text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                style={{ backgroundColor: '#334155' }}
              >
                <ChevronRight size={13} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Slide-in detail panel */}
      {selected && <DetailPanel finding={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
