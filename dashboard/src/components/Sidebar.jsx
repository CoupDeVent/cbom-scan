import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  Shield,
  LayoutDashboard,
  List,
  Tag,
  FolderTree,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/',          label: 'Overview',   Icon: LayoutDashboard, end: true },
  { to: '/findings',  label: 'Findings',   Icon: List },
  { to: '/categories',label: 'Categories', Icon: Tag },
  { to: '/filemap',   label: 'File Map',   Icon: FolderTree },
]

export function Sidebar({ collapsed, onToggle }) {
  return (
    <aside
      className="flex flex-col h-screen flex-shrink-0 transition-all duration-200"
      style={{
        width: collapsed ? 56 : 220,
        backgroundColor: '#1e293b',
        borderRight: '1px solid #334155',
      }}
    >
      {/* Logo */}
      <div
        className="flex items-center gap-2.5 px-3 flex-shrink-0"
        style={{ height: 56, borderBottom: '1px solid #334155' }}
      >
        <Shield size={20} style={{ color: '#6366f1', flexShrink: 0 }} />
        {!collapsed && (
          <span className="font-bold text-sm text-white truncate tracking-wide">
            cbom-scan
          </span>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1 p-2 flex-1 overflow-hidden">
        {NAV_ITEMS.map(({ to, label, Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className="flex items-center gap-3 px-2 py-2 rounded-md text-sm transition-colors duration-150 overflow-hidden"
            style={({ isActive }) =>
              isActive
                ? {
                    backgroundColor: '#1e1b4b',
                    borderLeft: '3px solid #6366f1',
                    color: '#a5b4fc',
                  }
                : {
                    borderLeft: '3px solid transparent',
                    color: '#94a3b8',
                  }
            }
          >
            {({ isActive }) => (
              <>
                <Icon
                  size={16}
                  style={{ color: isActive ? '#818cf8' : '#64748b', flexShrink: 0 }}
                />
                {!collapsed && (
                  <span className="truncate font-medium">{label}</span>
                )}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      <button
        onClick={onToggle}
        className="flex items-center justify-center py-3 text-slate-500 hover:text-slate-300 transition-colors flex-shrink-0"
        style={{ borderTop: '1px solid #334155' }}
        title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        {collapsed
          ? <ChevronRight size={15} />
          : <ChevronLeft size={15} />
        }
      </button>
    </aside>
  )
}
