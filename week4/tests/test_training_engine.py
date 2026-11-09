"""
Unit Tests for Week 4 Staff Training & Assessment Engine
Tests role-based modules, durations, practical exercises,
and 10-question competency evaluation scoring against the 85% threshold.
"""

import pytest
from week4.src.training_engine import TrainingEngine

def test_training_curriculum_loading():
    engine = TrainingEngine()
    summary = engine.get_summary()
    assert summary["total_modules"] == 5
    assert summary["total_training_hours"] == 46.0
    assert summary["total_questions"] == 10
    assert summary["passing_grade_percent"] == 85.0
    assert len(summary["roles_covered"]) == 5

def test_assessment_perfect_score():
    engine = TrainingEngine()
    # Perfect answer dict matching correct option index
    perfect_answers = {q.question_id: q.correct_option_index for q in engine.questions}
    res = engine.evaluate_answers(perfect_answers)
    assert res["correct_count"] == 10
    assert res["score_percent"] == 100.0
    assert res["passed"] is True

def test_assessment_failing_score():
    engine = TrainingEngine()
    # Intentionally select wrong options for half the questions
    flawed_answers = {}
    for i, q in enumerate(engine.questions):
        flawed_answers[q.question_id] = q.correct_option_index if i < 4 else (q.correct_option_index + 1) % len(q.options)
    res = engine.evaluate_answers(flawed_answers)
    assert res["score_percent"] < 85.0
    assert res["passed"] is False

def test_all_questions_have_references_and_explanations():
    engine = TrainingEngine()
    for q in engine.questions:
        assert len(q.options) == 4
        assert 0 <= q.correct_option_index < 4
        assert len(q.explanation) > 10
        assert len(q.guideline_reference) > 5
