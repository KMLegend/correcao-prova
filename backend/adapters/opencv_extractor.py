from typing import List, Tuple

import cv2
import numpy as np

from domain.entities import Answer, AnswerSheet
from domain.ports import AnswerExtractor
from domain.value_objects import AnswerChoice, QuestionNumber


COLUMN_LABELS = ["A", "B", "C", "D", "E"]


class ImagePreprocessor:
    """Responsável pelo pré-processamento da imagem."""

    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_threshold(self, grayscale_image: np.ndarray) -> np.ndarray:
        _, binary = cv2.threshold(
            grayscale_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        return binary


class GridDetector:
    """Responsável por detectar a grade de respostas na imagem."""

    MIN_CONTOUR_AREA_RATIO = 0.001
    MAX_CONTOUR_AREA_RATIO = 0.95

    def find_grid_contour(self, binary_image: np.ndarray) -> np.ndarray:
        """Encontra o maior contorno retangular (a grade de respostas)."""
        contours, _ = cv2.findContours(
            binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        image_area = binary_image.shape[0] * binary_image.shape[1]
        valid_contours = self._filter_valid_contours(contours, image_area)
        if not valid_contours:
            raise ValueError("Não foi possível detectar a grade de respostas na imagem.")
        return max(valid_contours, key=cv2.contourArea)

    def _filter_valid_contours(
        self, contours: tuple, image_area: int
    ) -> List[np.ndarray]:
        valid: List[np.ndarray] = []
        for contour in contours:
            area = cv2.contourArea(contour)
            ratio = area / image_area
            if ratio < self.MIN_CONTOUR_AREA_RATIO:
                continue
            if ratio > self.MAX_CONTOUR_AREA_RATIO:
                continue
            valid.append(contour)
        return valid

    def extract_grid_region(
        self, image: np.ndarray, contour: np.ndarray
    ) -> np.ndarray:
        """Recorta a região da grade a partir do contorno."""
        x, y, w, h = cv2.boundingRect(contour)
        return image[y : y + h, x : x + w]


class CellAnalyzer:
    """Responsável por analisar as células individuais da grade."""

    DEFAULT_DENSITY_THRESHOLD = 0.15

    def __init__(self, density_threshold: float = DEFAULT_DENSITY_THRESHOLD) -> None:
        self._density_threshold = density_threshold

    def slice_into_cells(
        self,
        grid_image: np.ndarray,
        num_rows: int,
        num_columns: int,
    ) -> List[List[np.ndarray]]:
        """Fatia a grade em uma matriz de células (linhas x colunas)."""
        height, width = grid_image.shape[:2]
        row_height = height // num_rows
        col_width = width // num_columns

        rows: List[List[np.ndarray]] = []
        for row_index in range(num_rows):
            row_cells: List[np.ndarray] = []
            for col_index in range(num_columns):
                cell = self._extract_cell(
                    grid_image, row_index, col_index, row_height, col_width
                )
                row_cells.append(cell)
            rows.append(row_cells)
        return rows

    def _extract_cell(
        self,
        grid_image: np.ndarray,
        row_index: int,
        col_index: int,
        row_height: int,
        col_width: int,
    ) -> np.ndarray:
        y_start = row_index * row_height
        y_end = (row_index + 1) * row_height
        x_start = col_index * col_width
        x_end = (col_index + 1) * col_width
        return grid_image[y_start:y_end, x_start:x_end]

    def is_marked(self, cell: np.ndarray) -> bool:
        """Verifica se uma célula está marcada com base na densidade de pixels."""
        total_pixels = cell.size
        if total_pixels == 0:
            return False
        white_pixels = cv2.countNonZero(cell)
        density = white_pixels / total_pixels
        return density > self._density_threshold


class OpenCVAnswerExtractor(AnswerExtractor):
    """Implementação do AnswerExtractor usando OpenCV.

    Pipeline: imagem → grayscale → threshold → detecção de grade →
    fatiamento em células → análise de densidade → AnswerSheet.
    """

    DEFAULT_NUM_QUESTIONS = 7
    DEFAULT_NUM_CHOICES = 5

    def __init__(
        self,
        num_questions: int = DEFAULT_NUM_QUESTIONS,
        num_choices: int = DEFAULT_NUM_CHOICES,
        density_threshold: float = CellAnalyzer.DEFAULT_DENSITY_THRESHOLD,
    ) -> None:
        self._num_questions = num_questions
        self._num_choices = num_choices
        self._preprocessor = ImagePreprocessor()
        self._grid_detector = GridDetector()
        self._cell_analyzer = CellAnalyzer(density_threshold)

    def extract(self, image_bytes: bytes) -> AnswerSheet:
        """Extrai as respostas marcadas da imagem do cartão-resposta."""
        image = self._decode_image(image_bytes)
        grayscale = self._preprocessor.convert_to_grayscale(image)
        binary = self._preprocessor.apply_threshold(grayscale)
        grid_contour = self._grid_detector.find_grid_contour(binary)
        grid_region = self._grid_detector.extract_grid_region(binary, grid_contour)
        cells = self._cell_analyzer.slice_into_cells(
            grid_region, self._num_questions, self._num_choices
        )
        answers = self._detect_answers(cells)
        return AnswerSheet(answers)

    def _decode_image(self, image_bytes: bytes) -> np.ndarray:
        np_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Não foi possível decodificar a imagem. Verifique o formato do arquivo.")
        return image

    def _detect_answers(self, cells: List[List[np.ndarray]]) -> List[Answer]:
        answers: List[Answer] = []
        for row_index, row_cells in enumerate(cells):
            detected = self._detect_marked_column(row_cells)
            if detected is None:
                continue
            question = QuestionNumber(row_index + 1)
            choice = AnswerChoice(COLUMN_LABELS[detected])
            answer = Answer(question, choice)
            answers.append(answer)
        return answers

    def _detect_marked_column(self, row_cells: List[np.ndarray]) -> int | None:
        """Encontra a coluna com maior densidade de marcação na linha.

        Retorna o índice da coluna ou None se nenhuma estiver marcada.
        """
        best_index = None
        best_density = 0.0
        for col_index, cell in enumerate(row_cells):
            if not self._cell_analyzer.is_marked(cell):
                continue
            density = cv2.countNonZero(cell) / cell.size
            if density > best_density:
                best_density = density
                best_index = col_index
        return best_index
