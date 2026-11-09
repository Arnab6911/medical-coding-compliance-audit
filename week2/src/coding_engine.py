"""Medical Coding Engine for Week 2: Medical Billing Process Simulation.

Performs transparent rule-based diagnosis-to-ICD-10-CM mapping, CPT procedure validation,
E/M level substantiation, and documentation completeness verification using
curated historical educational reference datasets (FY 2024 ICD-10-CM and CPT 2024).

Historical Reference Disclosure:
This software utilizes curated educational reference subsets. It is strictly intended
for educational billing workflow training and does NOT replace certified professional coding judgment.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple, Any


class CodingEngine:
    """Evaluates clinical documentation and validates ICD-10-CM and CPT code assignments."""

    def __init__(self, rules_dir: Optional[str] = None):
        if rules_dir is None:
            # Default to week2/data/rules or fallback to project data/rules
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(base_dir, "data", "rules")
            if os.path.exists(candidate):
                rules_dir = candidate
            else:
                rules_dir = os.path.join(os.path.dirname(base_dir), "data", "rules")

        self.rules_dir = rules_dir
        self.icd10_data = self._load_json("icd10_codes_fy2024.json")
        self.cpt_data = self._load_json("cpt_codes_2024.json")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.rules_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_icd10_entry(self, code: str) -> Optional[Dict[str, Any]]:
        clean = code.strip().upper()
        return self.icd10_data.get("codes", {}).get(clean)

    def get_cpt_entry(self, code: str) -> Optional[Dict[str, Any]]:
        clean = code.strip()
        return self.cpt_data.get("codes", {}).get(clean)

    def validate_encounter_coding(
        self,
        documented_diagnosis: str,
        assigned_icd10: str,
        clinical_notes: str,
        assigned_cpt: str,
        documentation_completeness: str = "Complete"
    ) -> Dict[str, Any]:
        """Validate coding decisions against clinical documentation and reference sets.

        Returns a dictionary with validation flags, specificity advice, and E/M status.
        """
        flags: List[str] = []
        is_supported = True
        notes_lower = (clinical_notes or "").lower()
        word_count = len((clinical_notes or "").split())

        # 1. ICD-10 Code Verification
        icd_codes = [c.strip() for c in assigned_icd10.split(";") if c.strip()]
        for code in icd_codes:
            entry = self.get_icd10_entry(code)
            if not entry:
                flags.append(f"ICD-10 code [{code}] is unverified in active FY2024 educational subset.")
                is_supported = False
            else:
                # Specificity check
                if entry.get("is_unspecified", False):
                    has_laterality = any(lat in notes_lower for lat in ["right", "left", "bilateral"])
                    if has_laterality:
                        flags.append(
                            f"Code [{code}] is unspecified, but documentation includes specific laterality. "
                            f"Consider specific alternative code."
                        )

        # 2. CPT Code Verification & Documentation Support
        cpt_codes = [c.strip() for c in assigned_cpt.split(";") if c.strip()]
        for cpt in cpt_codes:
            cpt_entry = self.get_cpt_entry(cpt)
            if not cpt_entry:
                flags.append(f"CPT code [{cpt}] is unverified in active 2024 educational subset.")
                is_supported = False
            else:
                requires_note = cpt_entry.get("requires_procedure_note", False)
                if requires_note:
                    kws = cpt_entry.get("keywords", [])
                    has_mention = any(kw.lower() in notes_lower for kw in kws)
                    if not has_mention:
                        flags.append(
                            f"CPT [{cpt} - {cpt_entry.get('description', '')}] billed without dedicated "
                            f"procedure/imaging report in notes."
                        )
                        is_supported = False

                # Medical necessity check
                compatible = cpt_entry.get("compatible_diagnoses", [])
                if compatible:
                    has_compat = any(icd in compatible for icd in icd_codes)
                    if not has_compat:
                        flags.append(
                            f"Potential medical necessity concern: assigned diagnosis [{assigned_icd10}] "
                            f"does not readily establish coverage for CPT [{cpt}]."
                        )

                # High Level E/M Check
                if cpt in ["99215", "99205"]:
                    if word_count < 15 or "refilled" in notes_lower:
                        flags.append(
                            f"Level 5 E/M CPT [{cpt}] requires high Medical Decision Making or qualifying time; "
                            f"documentation is terse ({word_count} words). Downcoding risk."
                        )

        # 3. Overall completeness check
        if word_count < 15:
            flags.append(f"Clinical documentation is brief ({word_count} words). Minimum standard recommended: 15 words.")

        return {
            "is_valid": is_supported and len([f for f in flags if "unverified" in f or "billed without" in f]) == 0,
            "flags": flags,
            "word_count": word_count,
            "icd10_count": len(icd_codes),
            "cpt_count": len(cpt_codes)
        }
