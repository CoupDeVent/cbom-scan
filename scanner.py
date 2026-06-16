#!/usr/bin/env python3
"""CBOM scanner that uses regex patterns defined in patterns.py."""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from patterns import CRYPTO_PATTERNS

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "javascript",
}

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", "venv", ".venv", "dist", "build"}


@dataclass
class Finding:
    id: str
    language: str
    category: str
    algorithm: str
    quantum_impact: str
    risk_level: str
    oid: Optional[str]
    notes: str
    file: str
    line: int
    snippet: str


def build_language_patterns() -> Dict[str, List[Dict]]:
    """Compile regex patterns from CRYPTO_PATTERNS grouped by language."""
    patterns: Dict[str, List[Dict]] = {}
    for pattern in CRYPTO_PATTERNS:
        language = pattern["language"]
        compiled_pattern = re.compile(pattern["regex"], re.IGNORECASE)
        patterns.setdefault(language, []).append({**pattern, "compiled": compiled_pattern})
    return patterns


LANGUAGE_PATTERNS = build_language_patterns()


def get_language_from_extension(path: Path) -> Optional[str]:
    """Return the scanner language for a file extension."""
    return LANGUAGE_BY_EXTENSION.get(path.suffix.lower())


def strip_inline_comment(line: str, language: str) -> str:
    """Remove inline comments from a source line for supported languages."""
    if language == "python":
        if "#" in line:
            return line.split("#", 1)[0]
    elif language in {"java", "javascript"}:
        if "//" in line:
            return line.split("//", 1)[0]
        if "/*" in line and "*/" in line:
            return line[: line.index("/*")] + line[line.index("*/") + 2 :]
    return line


def scan_file(filepath: Path, base: Path) -> List[Finding]:
    """Scan a single file and return all matching findings."""
    language = get_language_from_extension(filepath)
    if not language or language not in LANGUAGE_PATTERNS:
        return []

    try:
        file_content = filepath.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    findings: List[Finding] = []
    relative_path = str(filepath.relative_to(base))
    patterns = LANGUAGE_PATTERNS[language]

    for line_number, line_text in enumerate(file_content.splitlines(), start=1):
        stripped_line = line_text.strip()
        if not stripped_line:
            continue

        source_line = strip_inline_comment(line_text, language)
        if not source_line.strip():
            continue

        for pattern in patterns:
            if pattern["compiled"].search(source_line):
                findings.append(Finding(
                    id=pattern["id"],
                    language=language,
                    category=pattern["category"],
                    algorithm=pattern["algorithm"],
                    quantum_impact=pattern["quantum_impact"],
                    risk_level=pattern["risk_level"],
                    oid=pattern.get("oid"),
                    notes=pattern.get("notes", ""),
                    file=relative_path,
                    line=line_number,
                    snippet=stripped_line[:120],
                ))
    return findings


def scan_directory(target: Path) -> List[Finding]:
    """Scan all supported files under a directory recursively."""
    findings: List[Finding] = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in files:
            path = Path(root) / filename
            findings.extend(scan_file(path, target))
    return findings
