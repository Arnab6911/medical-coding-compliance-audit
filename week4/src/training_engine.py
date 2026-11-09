"""
Week 4 Staff Training & Assessment Engine
Manages role-based training curriculums, practical exercises,
and evaluates staff knowledge assessments against the 85% passing threshold.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from week4.src.models import TrainingModule, AssessmentQuestion

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class TrainingEngine:
    def __init__(self, curriculum_json: Optional[Path] = None):
        self.curriculum_json = curriculum_json or (DATA_DIR / "training_curriculum.json")
        self.curriculum_title: str = ""
        self.audience: str = ""
        self.passing_grade_percent: float = 85.0
        self.modules: List[TrainingModule] = []
        self.questions: List[AssessmentQuestion] = []
        self._load_curriculum()

    def _load_curriculum(self):
        if not self.curriculum_json.exists():
            raise FileNotFoundError(f"Training curriculum file not found: {self.curriculum_json}")

        with open(self.curriculum_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.curriculum_title = data.get("curriculum_title", "Integration Training Program")
        self.audience = data.get("audience", "Clinic Staff")
        self.passing_grade_percent = float(data.get("passing_grade_percent", 85.0))

        for m in data.get("modules", []):
            self.modules.append(TrainingModule(
                module_id=m["module_id"],
                target_role=m["target_role"],
                title=m["title"],
                duration_hours=float(m["duration_hours"]),
                learning_objectives=m["learning_objectives"],
                practical_exercises=m["practical_exercises"]
            ))

        for q in data.get("assessment_questions", []):
            self.questions.append(AssessmentQuestion(
                question_id=q["question_id"],
                target_role=q["target_role"],
                question=q["question"],
                options=q["options"],
                correct_option_index=int(q["correct_option_index"]),
                explanation=q["explanation"],
                guideline_reference=q["guideline_reference"]
            ))

    def evaluate_answers(self, user_answers: Dict[str, int]) -> Dict[str, Any]:
        """
        Evaluates submitted question responses against the answer key.
        user_answers is a dict of {question_id: selected_option_index}.
        """
        total = len(self.questions)
        correct_count = 0
        feedback = []

        for q in self.questions:
            selected = user_answers.get(q.question_id)
            is_correct = (selected == q.correct_option_index)
            if is_correct:
                correct_count += 1

            feedback.append({
                "question_id": q.question_id,
                "target_role": q.target_role,
                "question": q.question,
                "selected_option_index": selected,
                "selected_option_text": q.options[selected] if selected is not None and 0 <= selected < len(q.options) else "None / Unanswered",
                "correct_option_index": q.correct_option_index,
                "correct_option_text": q.options[q.correct_option_index],
                "is_correct": is_correct,
                "explanation": q.explanation,
                "guideline_reference": q.guideline_reference
            })

        score_percent = round((correct_count / total) * 100, 1) if total else 0.0
        passed = (score_percent >= self.passing_grade_percent)

        return {
            "total_questions": total,
            "correct_count": correct_count,
            "score_percent": score_percent,
            "passing_grade_percent": self.passing_grade_percent,
            "passed": passed,
            "feedback": feedback
        }

    def get_summary(self) -> Dict[str, Any]:
        total_hours = sum(m.duration_hours for m in self.modules)
        return {
            "title": self.curriculum_title,
            "target_audience": self.audience,
            "total_modules": len(self.modules),
            "total_training_hours": total_hours,
            "total_questions": len(self.questions),
            "passing_grade_percent": self.passing_grade_percent,
            "roles_covered": [m.target_role for m in self.modules]
        }
