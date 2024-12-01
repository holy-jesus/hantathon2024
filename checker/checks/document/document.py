import io

from aiohttp import ClientSession
from pypdf import PdfReader
from loguru import logger
import magic
import pdfplumber
import fitz

from ..types import Test, Result


class Document(Test):
    NAME = "PDF Документы"
    DESCRIPTION = """документы формата PDF, а также иные документы, 
представленные на официальном сайте, доступны для чтения при помощи 
вспомогательных технологий, включая программы экранного доступа, 
и размечены в соответствии с положениями национального стандарта 
Российской Федерации или на официальном сайте представлены альтернативные 
версии таких документов, доступные для чтения при помощи вспомогательных 
технологий, включая программы экранного доступа"""

    async def run(self):
        links = await self._page.eval_on_selector_all(
            "a[href], iframe", "elements => elements.map(e => e.href)"
        )

        # set чтобы оставить только уникальные ссылки и удалить дубликаты
        file_links = []
        total = 0
        total_percentage = 0
        for link in links:
            if link and link not in file_links and link.endswith((".pdf", ".docx")):
                file_links.append(link)
        if not file_links:
            return Result(Document, 100.0)
        if not any(link.endswith(".pdf") for link in file_links):
            return Result(Document, 100.0)
        else:
            for link in file_links:
                if link.endswith(".pdf"):
                    percentage = await self.__test_pdf(link)
                    total_percentage += percentage
                    total += 1
        return Result(Document, total_percentage / total)

    async def __test_pdf(self, file_link: str) -> float:
        async with ClientSession() as session:
            response = await session.get(file_link)
            content = await response.read()
        try:
            mime = magic.from_buffer(content, mime=True)
            if mime != "application/pdf":
                # Мы не можем проверить данный PDF файл, возвращаем будто всё норм
                logger.info("Скачанный файл не является PDF, пропускаю.")
                return 100.0
            text = self.__check_text_accessibility(content)
            struct = self.__check_struct(content)
            alt_text = self.__check_alt_text(content)
            metadata = self.__check_metadata(content)
            return sum((text, struct, alt_text, metadata)) / 4
        except Exception as e:
            logger.error("Произошла ошибка при обработке PDF файла")
            logger.exception(e)
            return 100.0

    def __check_text_accessibility(self, file: bytes) -> bool:
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            return 100.0 if any(page.extract_text() for page in pdf.pages) else 0.0

    def __check_struct(self, file: bytes) -> bool:
        pdf = PdfReader(io.BytesIO(file))
        return 100.0 if "/StructTreeRoot" in pdf.trailer["/Root"] else 0.0

    def __check_alt_text(self, file: bytes) -> bool:
        total = 0
        with_alt_text = 0
        doc = fitz.open(stream=file)
        for page_num in range(len(doc)):
            page = doc[page_num]
            for img in page.get_images(full=True):
                total += 1
                if "alt_text" in img:
                    with_alt_text += 1
        if not total:
            total = 1
            with_alt_text = 1
        return (with_alt_text / total) * 100
    
    def __check_metadata(self, file: bytes) -> bool:
        reader = PdfReader(io.BytesIO(file))
        metadata = reader.metadata
        required_fields = ['/Title', '/Author', '/Keywords']
        return 100.0 if any(field in metadata for field in required_fields) else 0.0
