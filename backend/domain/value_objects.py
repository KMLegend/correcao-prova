from __future__ import annotations


class AnswerChoice:
    """Value Object representando a letra da resposta (A-E)."""

    VALID_CHOICES = frozenset({"A", "B", "C", "D", "E"})

    def __init__(self, letter: str) -> None:
        normalized = letter.strip().upper()
        if normalized not in self.VALID_CHOICES:
            raise ValueError(
                f"Resposta inválida: '{letter}'. Escolhas válidas: {sorted(self.VALID_CHOICES)}"
            )
        self._letter = normalized

    def is_equal_to(self, other: AnswerChoice) -> bool:
        return self._letter == other._letter

    def value(self) -> str:
        return self._letter

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AnswerChoice):
            return NotImplemented
        return self._letter == other._letter

    def __hash__(self) -> int:
        return hash(self._letter)

    def __repr__(self) -> str:
        return f"AnswerChoice('{self._letter}')"


class QuestionNumber:
    """Value Object representando o número da questão (1+)."""

    def __init__(self, number: int) -> None:
        if not isinstance(number, int) or number < 1:
            raise ValueError(
                f"Número de questão inválido: {number}. Deve ser inteiro positivo."
            )
        self._number = number

    def value(self) -> int:
        return self._number

    def is_equal_to(self, other: QuestionNumber) -> bool:
        return self._number == other._number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuestionNumber):
            return NotImplemented
        return self._number == other._number

    def __hash__(self) -> int:
        return hash(self._number)

    def __repr__(self) -> str:
        return f"QuestionNumber({self._number})"

    def __lt__(self, other: QuestionNumber) -> bool:
        return self._number < other._number
