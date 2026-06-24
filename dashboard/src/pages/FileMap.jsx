import React, { useState, useEffect, useMemo } from 'react'
import { useLocation } from 'react-router-dom'
import { ChevronRight, ChevronDown, File, Folder } from 'lucide-react'
import { TopBar }      from '../components/TopBar'
import { RiskBadge, QuantumBadge } from '../components/Badge'
import { DetailPanel } from '../components/DetailPanel'
import { useReportContext } from '../context/ReportContext'
import { buildFileTree, getMaxRisk } from '../utils/parseReport'
import { RISK_COLORS } from '../utils/colors'

/* ─── Tree node ─────────────────────────────────────────────── */
function TreeNode({ name, node, allFindings, selectedFile, onSelect, depth = 0 }) {
  const [open, setOpen] = useState(depth < 2)
  const indent = depth * 14 + 8

  if (node.__isDir) {
    // Count all findings under this directory
    const prefix = name + '/'
    const dirFindings = allFindings.filter(f =>
      f.file.replace(/\\/g, '/').includes('/' + name + '/') ||
      f.file.replace(/\\/g, '/').startsWith(name + '/')
    )
    const maxRisk = getMaxRisk(dirFindings)
    const count   = dirFindings.length

    return (
      <div>
        <div
          className="flex items-center gap-1.5 py-1 rounded transition-colors cursor-pointer select-none"
          style={{ paddingLeft: indent, paddingRight: 8 }}
          onClick={() => setOpen(o => !o)}
          onMouseEnter={e => e.currentTarget.style.backgroundColor = '#334155'}
          onMouseLeave={e => e.currentTarget.style.backgroundColor = ''}
        >
          <span className="flex-shrink-0 text-slate-600">
            {open
              ? <ChevronDown  size={11} />
              : <ChevronRight size={11} />
            }
          </span>
          <Folder size={13} style={{ color: '#fbbf24', flexShrink: 0 }} />
          <span className="text-xs text-slate-300 truncate flex-1">{name}</span>
          {count > 0 && (
            <div className="flex items-center gap-1.5 flex-shrink-0">
              <div
                className="w-1.5 h-1.5 rounded-full"
                style={{ backgroundColor: RISK_COLORS[maxRisk] }}
              />
              <span className="text-xs text-slate-600">{count}</span>
            </div>
          )}
        </div>

        {open && (
          <div>
            {Object.entries(node.__children)
              .sort(([, a], [, b]) => {
                // Dirs first, then files
                if (a.__isDir && !b.__isDir) return -1
                if (!a.__isDir && b.__isDir) return 1
                return 0
              })
              .map(([k, v]) => (
                <TreeNode
                  key={k}
                  name={k}
                  node={v}
                  allFindings={allFindings}
                  selectedFile={selectedFile}
                  onSelect={onSelect}
                  depth={depth + 1}
                />
              ))
            }
          </div>
        )}
      </div>
    )
  }

  // File node
  const findings   = node.__findings
  const maxRisk    = getMaxRisk(findings)
  const filePath   = findings[0]?.file || ''
  const isSelected = selectedFile === filePath

  return (
    <div
      className="flex items-center gap-1.5 py-1 rounded cursor-pointer transition-colors select-none"
      style={{
        paddingLeft:     indent + 16,
        paddingRight:    8,
        backgroundColor: isSelected ? '#1e1b4b' : '',
      }}
      onClick={() => onSelect(filePath)}
      onMouseEnter={e => { if (!isSelected) e.currentTarget.style.backgroundColor = '#334155' }}
      onMouseLeave={e => { if (!isSelected) e.currentTarget.style.backgroundColor = '' }}
    >
      <File size={12} style={{ color: isSelected ? '#818cf8' : '#475569', flexShrink: 0 }} />
      <span
        className={`text-xs truncate flex-1 ${isSelected ? 'text-indigo-300 font-medium' : 'text-slate-400'}`}
        title={filePath}
      >
        {name}
      </span>
      <div
        className="w-1.5 h-1.5 rounded-full flex-shrink-0"
        style={{ backgroundColor: RISK_COLORS[maxRisk] }}
      />
      <span className="text-xs text-slate-600 flex-shrink-0 ml-1">{findings.length}</span>
    </div>
  )
}

/* ─── Page ───────────────────────────────────────────────────── */
export function FileMap() {
  const { report }  = useReportContext()
  const location    = useLocation()
  const [selectedFile,    setSelectedFile]    = useState(null)
  const [selectedFinding, setSelectedFinding] = useState(null)

  // Pre-select file coming from Overview table click
  useEffect(() => {
    if (location.state?.selectedFile) {
      setSelectedFile(location.state.selectedFile)
      // Clear location state so it doesn't re-trigger on re-render
      window.history.replaceState({}, '')
    }
  }, [location.state])

  if (!report) return null

  const tree = useMemo(() => buildFileTree(report.findings), [report.findings])

  const fileFindings = useMemo(() =>
    selectedFile
      ? report.findings.filter(f => f.file === selectedFile).sort((a, b) => a.line - b.line)
      : [],
    [report.findings, selectedFile]
  )

  const maxRisk = selectedFile ? getMaxRisk(fileFindings) : null

  return (
    <div className="flex flex-1 overflow-hidden">
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopBar title="File Map" />

        <div className="flex flex-1 overflow-hidden">

          {/* File tree panel */}
          <div
            className="flex-shrink-0 overflow-y-auto py-2"
            style={{ width: 280, borderRight: '1px solid #334155', backgroundColor: '#1e293b' }}
          >
            {Object.entries(tree)
              .sort(([, a], [, b]) => {
                if (a.__isDir && !b.__isDir) return -1
                if (!a.__isDir && b.__isDir) return 1
                return 0
              })
              .map(([k, v]) => (
                <TreeNode
                  key={k}
                  name={k}
                  node={v}
                  allFindings={report.findings}
                  selectedFile={selectedFile}
                  onSelect={(path) => { setSelectedFile(path); setSelectedFinding(null) }}
                />
              ))
            }
          </div>

          {/* File detail panel */}
          <div className="flex-1 overflow-y-auto p-6">
            {!selectedFile ? (
              <div className="flex items-center justify-center h-full">
                <p className="text-sm text-slate-600">
                  Select a file to inspect its cryptographic findings.
                </p>
              </div>
            ) : (
              <div className="flex flex-col gap-5">

                {/* File header */}
                <div className="flex items-center gap-3 flex-wrap">
                  <span className="font-mono text-sm text-slate-200 break-all">{selectedFile}</span>
                  {maxRisk && <RiskBadge level={maxRisk} />}
                  <span className="text-xs text-slate-500">
                    {fileFindings.length} finding{fileFindings.length !== 1 ? 's' : ''}
                  </span>
                </div>

                {/* Timeline */}
                <div className="flex flex-col gap-2">
                  {fileFindings.map(f => (
                    <div
                      key={f.uid}
                      onClick={() => setSelectedFinding(f)}
                      className="flex items-center gap-4 p-3 rounded-lg cursor-pointer transition-colors"
                      style={{
                        backgroundColor: '#1e293b',
                        border:          '1px solid #334155',
                        borderLeft:      `3px solid ${RISK_COLORS[f.riskLevel] || '#334155'}`,
                      }}
                      onMouseEnter={e => e.currentTarget.style.backgroundColor = '#293548'}
                      onMouseLeave={e => e.currentTarget.style.backgroundColor = '#1e293b'}
                    >
                      {/* Line number */}
                      <span
                        className="font-mono text-xs text-slate-500 flex-shrink-0 text-right"
                        style={{ minWidth: 36 }}
                      >
                        :{f.line}
                      </span>

                      {/* Algorithm */}
                      <span className="text-slate-200 font-medium text-sm flex-shrink-0 w-32 truncate">
                        {f.algorithm}
                      </span>

                      {/* Badges */}
                      <RiskBadge    level={f.riskLevel} />
                      <QuantumBadge impact={f.quantumImpact} />

                      {/* Snippet (truncated, tooltip on hover) */}
                      {f.snippet && (
                        <span
                          className="font-mono text-xs text-slate-500 truncate flex-1 ml-2"
                          title={f.snippet}
                        >
                          {f.snippet}
                        </span>
                      )}
                    </div>
                  ))}
                </div>

              </div>
            )}
          </div>

        </div>
      </div>

      {selectedFinding && (
        <DetailPanel finding={selectedFinding} onClose={() => setSelectedFinding(null)} />
      )}
    </div>
  )
}
