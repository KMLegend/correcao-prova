from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

from domain.value_objects import AnswerChoice, QuestionNumber


class CorrectionStatus(Enum):
    """Status de correção de uma questão."""
    CORRECT = "Acerto"
    INCORRECT = "Erro"


class Answer:
    """Entidade representando uma resposta individual (questão + escolha)."""

    def __init__(self, question: QuestionNumber, choice: AnswerChoice) -> None:
        self._question = question
        self._choice = choice

    def matches(self, other: Answer) -> bool:
        """Verifica se esta resposta corresponde à outra (Tell, Don't Ask)."""
        return self._choice.is_equal_to(other._choice)

    def question(self) -> QuestionNumber:
        return self._question

    def choice_value(self) -> str:
        return self._choice.value()

    def __repr__(self) -> str:
        return f"Answer({self._question}, {self._choice})"


class AnswerSheet:
    """Coleção de primeira classe encapsulando uma lista de respostas.

    Segue Object Calisthenics regra 4: classe que contém coleção
    não possui outros comportamentos além de operar sobre a coleção.
    """

    def __init__(self, answers: List[Answer]) -> None:
        self._answers = sorted(answers, key=lambda a: a.question())

    def compare_with(self, answer_key: AnswerSheet) -> List[CorrectionResult]:
        """Compara este cartão-resposta com o gabarito (Tell, Don't Ask).

        Retorna lista de CorrectionResult para cada questão.
        """
        key_map = answer_key._build_answer_map()
        results: List[CorrectionResult] = []
        for student_answer in self._answers:
            question_number = student_answer.question()
            correct_answer = key_map.get(question_number)
            if correct_answer is None:
                continue
            status = self._determine_status(student_answer, correct_answer)
            result = CorrectionResult(
                question=question_number,
                student_answer=student_answer.choice_value(),
                correct_answer=correct_answer.choice_value(),
                status=status,
            )
            results.append(result)
        return results

    def _build_answer_map(self) -> dict:
        answer_map: dict = {}
        for answer in self._answers:
            answer_map[answer.question()] = answer
        return answer_map

    def _determine_status(
        self, student_answer: Answer, correct_answer: Answer
    ) -> CorrectionStatus:
        if student_answer.matches(correct_answer):
            return CorrectionStatus.CORRECT
        return CorrectionStatus.INCORRECT

    def count(self) -> int:
        return len(self._answers)

    def __repr__(self) -> str:
        return f"AnswerSheet({len(self._answers)} answers)"


@dataclass(frozen=True)
class CorrectionResult:
    """Resultado da correção de uma questão individual."""

    question: QuestionNumber
    student_answer: str
    correct_answer: str
    status: CorrectionStatus

    def is_correct(self) -> bool:
        return self.status == CorrectionStatus.CORRECT

    def question_number(self) -> int:
        return self.question.value()

    def status_label(self) -> str:
        return self.status.value

    def to_dict(self) -> dict:
        return {
            "questao": self.question_number(),
            "resposta_aluno": self.student_answer,
            "resposta_correta": self.correct_answer,
            "status": self.status_label(),
        }
