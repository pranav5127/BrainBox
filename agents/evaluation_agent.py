import json

from utils.evaluation.evaluation_service import ExamEvaluationService


def evaluate_agent(file_path):
    result = ExamEvaluationService.evaluate_exam_from_file(file_path)
    return json.dumps(result, indent=4)