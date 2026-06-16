#!/usr/bin/env python3
"""Report generation utilities for the CBOM scanner."""

import json
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from scanner import Finding


def build_report(findings: List[Finding], target: Path) -> Dict:
    """Build a CycloneDX v1.7 BOM report from scanner findings."""
    artifacts = []
    for finding in findings:
        artifact = {
            "bom-ref": f"cbom:{finding.id}:{finding.file}:{finding.line}",
            "type": "cryptographic-asset",
            "name": finding.algorithm,
            "description": finding.notes or "",
            "properties": [
                {"name": "cbom:ruleId", "value": str(finding.id)},
                {"name": "cbom:language", "value": str(finding.language)},
                {"name": "cbom:category", "value": str(finding.category)},
                {"name": "cbom:quantumImpact", "value": str(finding.quantum_impact)},
                {"name": "cbom:riskLevel", "value": str(finding.risk_level)},
                {"name": "cbom:file", "value": str(finding.file)},
                {"name": "cbom:line", "value": str(finding.line)},
                {"name": "cbom:snippet", "value": str(finding.snippet)},
            ],
        }
        if finding.oid:
            artifact["properties"].append({"name": "cbom:oid", "value": str(finding.oid)})
        artifacts.append(artifact)

    report = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.7",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tools": [
                {
                    "vendor": "cbom-scan",
                    "name": "CBOM Scanner",
                    "version": "1.0.0",
                }
            ],
            "component": {
                "type": "application",
                "name": target.name,
                "version": "1.0.0",
                "description": f"Cryptographic assets inventory for {target.name}",
                "properties": [
                    {"name": "cbom:targetPath", "value": str(target.resolve())},
                    {"name": "cbom:totalFindings", "value": str(len(findings))},
                ],
            },
        },
        "components": artifacts,
    }

    return report


def save_report(report: Dict, output_path: str) -> None:
    """Write the report dictionary to the specified JSON file."""
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
