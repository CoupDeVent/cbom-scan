export const RISK_COLORS = {
  critical: '#ef4444',
  high:     '#f97316',
  medium:   '#eab308',
  low:      '#3b82f6',
  info:     '#6b7280',
}

export const QUANTUM_COLORS = {
  shor_breakable:  '#ef4444',
  grover_weakened: '#f97316',
  already_weak:    '#eab308',
  quantum_safe:    '#22c55e',
}

export const RISK_ORDER   = ['critical', 'high', 'medium', 'low', 'info']
export const QUANTUM_ORDER = ['shor_breakable', 'grover_weakened', 'already_weak', 'quantum_safe']
export const CATEGORIES   = ['symmetric', 'asymmetric', 'hash', 'mac', 'kdf', 'pqc']
export const LANGUAGES    = ['python', 'java', 'javascript']

export const RISK_LABELS = {
  critical: 'Critical',
  high:     'High',
  medium:   'Medium',
  low:      'Low',
  info:     'Info',
}

export const QUANTUM_LABELS = {
  shor_breakable:  'Shor-Breakable',
  grover_weakened: 'Grover-Weakened',
  already_weak:    'Already Weak',
  quantum_safe:    'Quantum-Safe',
}
