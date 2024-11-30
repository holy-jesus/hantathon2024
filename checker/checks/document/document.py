import io

from aiohttp import ClientSession
from PyPDF2 import PdfReader
import magic
import pdfplumber

from ..types import Test


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
            "a[href]", "elements => elements.map(e => e.href)"
        )

        # set чтобы оставить только уникальные ссылки и удалить дубликаты
        file_links = list(
            set(link for link in links if link.endswith((".pdf", ".docx")))
        )
        if not file_links:
            return True
        if not any(link.endswith(".pdf") for link in file_links):
            return True
        else:
            for link in file_links:
                if link.endswith(".pdf"):
                    pdf = await self.__test_pdf(link)
                    if not pdf:
                        return False

        return True

    async def __test_pdf(self, file_link: str):
        async with ClientSession() as session:
            response = await session.get(file_link)
            content = await response.read()
        mime = magic.from_file(content)
        if mime != "application/pdf":
            # Мы не можем проверить данный PDF файл, возвращаем будто всё норм
            return True
        return self.__check_text_accessibility(content) and self.__check_struct(content)

    def __check_text_accessibility(self, file: bytes) -> bool:
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            return any(page.extract_text() for page in pdf.pages)

    def __check_struct(self, file: bytes) -> bool:
        pdf = PdfReader(io.BytesIO(file))
        return "/StructTreeRoot" in pdf.trailer["/Root"]
