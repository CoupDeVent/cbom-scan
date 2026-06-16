#!/usr/bin/env python3
"""Report generation utilities for the CBOM scanner."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from scanner import Finding


def build_report(findings: List[Finding], target: Path) -> Dict:
    """Build a JSON report summary from scanner findings."""
    by_language: Dict[str, int] = {}
    by_category: Dict[str, int] = {}
    by_impact: Dict[str, int] = {}
    by_risk: Dict[str, int] = {}

    for finding in findings:
        by_language[finding.language] = by_language.get(finding.language, 0) + 1
        by_category[finding.category] = by_category.get(finding.category, 0) + 1
        by_impact[finding.quantum_impact] = by_impact.get(finding.quantum_impact, 0) + 1
        by_risk[finding.risk_level] = by_risk.get(finding.risk_level, 0) + 1

    return {
        "target": str(target.resolve()),
        "findings": [asdict(f) for f in findings],
        "summary": {
            "total_findings": len(findings),
            "by_language": by_language,
            "by_category": by_category,
            "by_quantum_impact": by_impact,
            "by_risk_level": by_risk,
        },
    }


def save_report(report: Dict, output_path: str) -> None:
    """Write the report dictionary to the specified JSON file."""
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
