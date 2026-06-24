import React, { createContext, useContext, useState } from 'react'

const ReportContext = createContext(null)

export function ReportProvider({ children }) {
  const [report, setReport] = useState(null)
  return (
    <ReportContext.Provider value={{ report, setReport }}>
      {children}
    </ReportContext.Provider>
  )
}

export function useReportContext() {
  return useContext(ReportContext)
}
