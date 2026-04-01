from typing import List

from domain.entities import AnswerSheet, CorrectionResult
from domain.ports import AnswerExtractor


class EvaluateExamUseCase:
    """Caso de uso principal: avalia o cartão-resposta do aluno
    comparando com o gabarito.

    Recebe duas abstrações (AnswerExtractor) para o gabarito e
    para o cartão do aluno, seguindo DIP.
    """

    def __init__(self, extractor: AnswerExtractor) -> None:
        self._extractor = extractor

    def execute(
        self,
        answer_key_image: bytes,
        student_card_image: bytes,
    ) -> List[CorrectionResult]:
        """Executa a correção automática.

        Args:
            answer_key_image: Bytes da imagem do gabarito.
            student_card_image: Bytes da imagem do cartão-resposta do aluno.

        Returns:
            Lista de CorrectionResult com o resultado de cada questão.
        """
        answer_key = self._extract_answer_key(answer_key_image)
        student_sheet = self._extract_student_answers(student_card_image)
        return student_sheet.compare_with(answer_key)

    def _extract_answer_key(self, image_bytes: bytes) -> AnswerSheet:
        return self._extractor.extract(image_bytes)

    def _extract_student_answers(self, image_bytes: bytes) -> AnswerSheet:
        return self._extractor.extract(image_bytes)

    def execute_with_json_key(
        self,
        answer_key_sheet: AnswerSheet,
        student_card_image: bytes,
    ) -> List[CorrectionResult]:
        """Executa a correção usando um gabarito já em formato AnswerSheet (JSON).

        Args:
            answer_key_sheet: AnswerSheet do gabarito (parseado de JSON).
            student_card_image: Bytes da imagem do cartão-resposta do aluno.

        Returns:
            Lista de CorrectionResult com o resultado de cada questão.
        """
        student_sheet = self._extract_student_answers(student_card_image)
        return student_sheet.compare_with(answer_key_sheet)
