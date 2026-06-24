import React, { useState } from 'react'
import { Shield, Upload } from 'lucide-react'
import { parseReport } from '../utils/parseReport'
import { useReportContext } from '../context/ReportContext'

export function WelcomeScreen() {
  const { setReport } = useReportContext()
  const [error, setError]     = useState(null)
  const [dragging, setDragging] = useState(false)

  const handleElectronOpen = async () => {
    setError(null)
    try {
      const result = await window.electronAPI.openFileDialog()
      if (!result) return
      if (result.error) { setError(result.error); return }
      setReport(parseReport(result.data))
    } catch (e) {
      setError(e.message)
    }
  }

  // Fallback for browser dev mode (no electronAPI)
  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (!file || !file.name.endsWith('.json')) {
      setError('Please drop a .json file.')
      return
    }
    const reader = new FileReader()
    reader.onload = (ev) => {
      try {
        setReport(parseReport(JSON.parse(ev.target.result)))
      } catch (err) {
        setError(err.message)
      }
    }
    reader.readAsText(file)
  }

  const handleClick = () => {
    if (window.electronAPI) handleElectronOpen()
  }

  return (
    <div
      className="flex flex-col items-center justify-center h-full gap-10"
      style={{ backgroundColor: '#0f172a' }}
    >
      {/* Branding */}
      <div className="flex flex-col items-center gap-3">
        <div
          className="flex items-center justify-center w-16 h-16 rounded-2xl"
          style={{ backgroundColor: '#312e81' }}
        >
          <Shield size={32} style={{ color: '#818cf8' }} />
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">CBOM Scan Dashboard</h1>
        <p className="text-sm text-slate-400 text-center max-w-sm">
          Load a CycloneDX v1.7 JSON report produced by cbom-scan to visualize
          your cryptographic asset inventory and quantum exposure.
        </p>
      </div>

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={handleClick}
        className="flex flex-col items-center gap-4 p-14 rounded-2xl cursor-pointer transition-all duration-150"
        style={{
          border: `2px dashed ${dragging ? '#6366f1' : '#334155'}`,
          backgroundColor: dragging ? '#1e1b4b' : '#1e293b22',
          minWidth: 380,
        }}
      >
        <Upload
          size={36}
          style={{ color: dragging ? '#818cf8' : '#475569', transition: 'color 0.15s' }}
        />
        <div className="text-center">
          <p className="text-slate-200 font-medium">Drop your cbom-scan report here</p>
          <p className="text-slate-500 text-sm mt-1">or click to browse</p>
        </div>
        <button
          className="px-5 py-2 rounded-lg text-sm font-semibold text-white transition-colors"
          style={{ backgroundColor: '#4f46e5' }}
          onMouseEnter={e => e.currentTarget.style.backgroundColor = '#4338ca'}
          onMouseLeave={e => e.currentTarget.style.backgroundColor = '#4f46e5'}
        >
          Open Report
        </button>
      </div>

      {error && (
        <div
          className="px-5 py-3 rounded-lg text-sm text-center max-w-md"
          style={{ backgroundColor: '#7f1d1d22', border: '1px solid #991b1b', color: '#fca5a5' }}
        >
          {error}
        </div>
      )}

      <p className="text-xs text-slate-600">
        File · Open Report  (Ctrl+O)
      </p>
    </div>
  )
}
