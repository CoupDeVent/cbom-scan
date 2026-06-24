import React, { useState, useEffect } from 'react'
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Sidebar }      from './components/Sidebar'
import { WelcomeScreen } from './components/WelcomeScreen'
import { Overview }     from './pages/Overview'
import { Findings }     from './pages/Findings'
import { Categories }   from './pages/Categories'
import { FileMap }      from './pages/FileMap'
import { ReportProvider, useReportContext } from './context/ReportContext'
import { parseReport }  from './utils/parseReport'

function AppShell() {
  const { report, setReport } = useReportContext()
  const [collapsed, setCollapsed] = useState(false)

  // Wire up Electron native menu events
  useEffect(() => {
    if (!window.electronAPI) return

    const handleOpen = async () => {
      try {
        const result = await window.electronAPI.openFileDialog()
        if (!result || result.error) return
        setReport(parseReport(result.data))
      } catch (e) {
        console.error('Failed to open report:', e)
      }
    }

    const handleClose = () => setReport(null)

    window.electronAPI.onMenuOpenReport(handleOpen)
    window.electronAPI.onMenuCloseReport(handleClose)

    return () => {
      window.electronAPI.removeAllListeners('menu-open-report')
      window.electronAPI.removeAllListeners('menu-close-report')
    }
  }, [setReport])

  if (!report) {
    return <WelcomeScreen />
  }

  return (
    <div className="flex h-screen overflow-hidden" style={{ backgroundColor: '#0f172a' }}>
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Routes>
          <Route path="/"           element={<Overview />}    />
          <Route path="/findings"   element={<Findings />}    />
          <Route path="/categories" element={<Categories />}  />
          <Route path="/filemap"    element={<FileMap />}     />
          <Route path="*"           element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <ReportProvider>
      <HashRouter>
        <AppShell />
      </HashRouter>
    </ReportProvider>
  )
}
