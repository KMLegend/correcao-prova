from typing import Set

from fastapi import UploadFile


ALLOWED_EXTENSIONS: Set[str] = {"image/png", "image/jpeg", "image/jpg"}
MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB


class FileValidationError(Exception):
    """Exceção para erros de validação de arquivo."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class FileValidator:
    """Responsável por validar arquivos enviados pelo usuário."""

    def validate(self, file: UploadFile) -> None:
        """Valida tipo e tamanho do arquivo."""
        self._validate_content_type(file)

    def _validate_content_type(self, file: UploadFile) -> None:
        content_type = file.content_type or ""
        if content_type not in ALLOWED_EXTENSIONS:
            raise FileValidationError(
                f"Formato de arquivo não suportado: '{content_type}'. "
                f"Formatos aceitos: PNG, JPG, JPEG."
            )

    async def validate_size(self, file_bytes: bytes) -> None:
        """Valida o tamanho do arquivo após leitura."""
        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            size_mb = len(file_bytes) / (1024 * 1024)
            raise FileValidationError(
                f"Arquivo muito grande ({size_mb:.1f} MB). "
                f"Tamanho máximo: {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
            )
