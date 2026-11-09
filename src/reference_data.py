"""Reference data management for Medical Coding Compliance Audit Simulation.

Loads and maintains version-aware ICD-10-CM and CPT code subsets along with
official regulatory guidelines and threshold configurations.
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List


DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "rules"


class ReferenceDataManager:
    """Manages version-aware reference datasets and validation configurations."""

    def __init__(self, rules_dir: Optional[Path] = None):
        self.rules_dir = Path(rules_dir) if rules_dir else DEFAULT_DATA_DIR
        self.icd10_data: Dict[str, Any] = {}
        self.cpt_data: Dict[str, Any] = {}
        self.rules_config: Dict[str, Any] = {}
        self.load_all()

    def load_all(self) -> None:
        """Load ICD-10, CPT, and audit configuration JSON files."""
        icd_path = self.rules_dir / "icd10_codes_fy2024.json"
        cpt_path = self.rules_dir / "cpt_codes_2024.json"
        config_path = self.rules_dir / "audit_rules_config.json"

        if icd_path.exists():
            with open(icd_path, "r", encoding="utf-8") as f:
                self.icd10_data = json.load(f)
        else:
            self.icd10_data = {"version": "Unknown", "codes": {}}

        if cpt_path.exists():
            with open(cpt_path, "r", encoding="utf-8") as f:
                self.cpt_data = json.load(f)
        else:
            self.cpt_data = {"version": "Unknown", "codes": {}}

        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self.rules_config = json.load(f)
        else:
            self.rules_config = {
                "standard_citations": {},
                "documentation_thresholds": {
                    "min_note_word_count_standard": 15,
                    "min_note_word_count_high_em": 45,
                    "signature_keywords": ["electronically signed", "authenticated by", "signed by"]
                }
            }

    @property
    def icd10_version(self) -> str:
        return self.icd10_data.get("version", "ICD-10-CM FY 2024 (Educational Subset)")

    @property
    def cpt_version(self) -> str:
        return self.cpt_data.get("version", "CPT 2024 (Educational Subset)")

    @property
    def rules_version(self) -> str:
        return self.rules_config.get("rules_version", "2024.1")

    def get_icd10_entry(self, code: str) -> Optional[Dict[str, Any]]:
        """Lookup an ICD-10-CM code definition in reference dataset."""
        if not code:
            return None
        clean_code = code.strip().upper()
        return self.icd10_data.get("codes", {}).get(clean_code)

    def get_cpt_entry(self, code: str) -> Optional[Dict[str, Any]]:
        """Lookup a CPT code definition in reference dataset."""
        if not code:
            return None
        clean_code = code.strip().upper()
        return self.cpt_data.get("codes", {}).get(clean_code)

    def get_citation(self, citation_key: str, default: str = "") -> str:
        """Retrieve standard official citation text by rule identifier."""
        return self.rules_config.get("standard_citations", {}).get(citation_key, default)

    def get_thresholds(self) -> Dict[str, Any]:
        """Retrieve documentation audit thresholds."""
        return self.rules_config.get("documentation_thresholds", {})

    def get_severity_definitions(self) -> Dict[str, str]:
        """Retrieve descriptions of severity categories."""
        return self.rules_config.get("severity_definitions", {})

    def find_matching_icd_by_text(self, text: str) -> List[str]:
        """Find potential ICD-10 codes that match keywords in the text."""
        matched = []
        lower_text = text.lower()
        for code, details in self.icd10_data.get("codes", {}).items():
            keywords = details.get("keywords", [])
            for kw in keywords:
                if kw.lower() in lower_text:
                    matched.append(code)
                    break
        return matched


# Global singleton helper
_DEFAULT_MANAGER: Optional[ReferenceDataManager] = None


def get_reference_manager() -> ReferenceDataManager:
    """Return singleton ReferenceDataManager instance."""
    global _DEFAULT_MANAGER
    if _DEFAULT_MANAGER is None:
        _DEFAULT_MANAGER = ReferenceDataManager()
    return _DEFAULT_MANAGER
