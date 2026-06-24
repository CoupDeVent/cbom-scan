import React from 'react'
import { useReportContext } from '../context/ReportContext'

function formatDate(iso) {
  if (!iso) return '-'
  try {
    return new Date(iso).toLocaleString('en-GB', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    })
  } catch {
    return iso
  }
}

export function TopBar({ title }) {
  const { report } = useReportContext()
  return (
    <div
      className="flex items-center justify-between px-6 flex-shrink-0"
      style={{ height: 56, borderBottom: '1px solid #334155', backgroundColor: '#1e293b' }}
    >
      <h1 className="text-sm font-semibold text-white tracking-wide">{title}</h1>
      {report && (
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span className="text-slate-200 font-medium">{report.projectName}</span>
          <span className="text-slate-600">·</span>
          <span>Scanned {formatDate(report.timestamp)}</span>
          <span className="text-slate-600">·</span>
          <span>cbom-scan v{report.toolVersion}</span>
        </div>
      )}
    </div>
  )
}
