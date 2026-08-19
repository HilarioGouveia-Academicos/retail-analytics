"""Módulo de extração e processamento de documentos PDF."""

from pathlib import Path
from typing import Dict, Any, Union
import io
from pypdf import PdfReader
from retail_analytics.config import logger


class PDFDocumentReader:
    """Extrai texto e metadados de arquivos PDF para contexto do Agente."""

    def __init__(self, file_source: Union[Path, io.BytesIO, bytes]) -> None:
        self.file_source = file_source

    def extract_text(self, max_pages: int = 20) -> Dict[str, Any]:
        """Lê o PDF e retorna o conteúdo textual concatenado e metadados."""
        try:
            reader = PdfReader(self.file_source)
            num_pages = len(reader.pages)
            logger.info(f"Processando PDF com {num_pages} página(s)...")

            extracted_text = []
            for idx, page in enumerate(reader.pages[:max_pages]):
                page_text = page.extract_text() or ""
                extracted_text.append(f"--- PÁGINA {idx + 1} ---\n{page_text.strip()}")

            full_content = "\n\n".join(extracted_text)
            return {
                "total_pages": num_pages,
                "pages_read": min(num_pages, max_pages),
                "content": full_content,
            }

        except Exception as exc:
            logger.exception("Falha ao realizar a leitura do arquivo PDF.")
            raise RuntimeError(f"Erro ao processar PDF: {exc}") from exc