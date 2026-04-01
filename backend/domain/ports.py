from abc import ABC, abstractmethod

from domain.entities import AnswerSheet


class AnswerExtractor(ABC):
    """Porta (interface) para extração de respostas de uma imagem.

    Segue DIP (Dependency Inversion Principle): os casos de uso
    dependem desta abstração, não da implementação concreta (OpenCV).
    """

    @abstractmethod
    def extract(self, image_bytes: bytes) -> AnswerSheet:
        """Extrai as respostas marcadas de uma imagem.

        Args:
            image_bytes: Bytes da imagem do cartão-resposta/gabarito.

        Returns:
            AnswerSheet contendo as respostas detectadas.
        """
        ...
