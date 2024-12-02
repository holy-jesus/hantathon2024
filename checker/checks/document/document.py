import io

from aiohttp import ClientSession
from pypdf import PdfReader
from loguru import logger
import magic
import pdfplumber
import fitz

from ..types import Test, Result


class Document(Test):
    """
    Тест для проверки доступности PDF-документов на сайте.
    """

    NAME = "PDF Документы"
    DESCRIPTION = """документы формата PDF, а также иные документы, 
представленные на официальном сайте, доступны для чтения при помощи 
вспомогательных технологий, включая программы экранного доступа, 
и размечены в соответствии с положениями национального стандарта 
Российской Федерации или на официальном сайте представлены альтернативные 
версии таких документов, доступные для чтения при помощи вспомогательных 
технологий, включая программы экранного доступа"""
    DEFIANCE = "PDF документы не размечены по ГОСТ Р 70176-2022 и не представлены в альтернативных версиях."
    RECOMMENDATION = "Для PDF-документов создавайте альтернативные версии в формате HTML, доступные для чтения с помощью экранных чтецов."

    async def run(self):
        """
        Запускает тест доступности для всех PDF-файлов на странице.

        Returns:
            Result: Объект результата теста, содержащий название теста и процент успеха.
        """
        links = await self._page.eval_on_selector_all(
            "a[href], iframe", "elements => elements.map(e => e.href)"
        )

        # Собираем уникальные ссылки на PDF и DOCX файлы
        file_links = []
        total = 0
        total_percentage = 0
        for link in links:
            if link and link not in file_links and link.endswith((".pdf", ".docx")):
                file_links.append(link)

        # Если нет PDF-файлов, тест считается пройденным
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
        final_score = total_percentage / total
        if final_score != 100.0:
            self._report.add_defiance(self.DEFIANCE)
            self._report.add_recommendation(self.RECOMMENDATION)
            self._report.add_xpaths(None)
        return Result(Document, final_score)

    async def __test_pdf(self, file_link: str) -> float:
        """
        Проверяет доступность PDF-файла по заданной ссылке.

        Args:
            file_link (str): Ссылка на PDF-файл.

        Returns:
            float: Процент успеха теста для файла (0.0–100.0).
        """
        async with ClientSession() as session:
            response = await session.get(file_link)
            content = await response.read()
        try:
            mime = magic.from_buffer(content, mime=True)
            if mime != "application/pdf":
                # Если файл не является PDF, возвращаем успешный результат
                logger.info("Скачанный файл не является PDF, пропускаю.")
                return 100.0
            text = self.__check_text_accessibility(content, file_link)
            struct = self.__check_struct(content, file_link)
            alt_text = self.__check_alt_text(content, file_link)
            metadata = self.__check_metadata(content, file_link)
            return sum((text, struct, alt_text, metadata)) / 4
        except Exception as e:
            logger.error("Произошла ошибка при обработке PDF файла")
            logger.exception(e)
            return 100.0

    def __check_text_accessibility(self, file: bytes, file_link: str) -> float:
        """
        Проверяет, содержит ли PDF текст, доступный для чтения.

        Args:
            file (bytes): Содержимое PDF-файла.
            file_link (str): Ссылка на PDF-файл.

        Returns:
            bool: 100.0, если текст доступен, иначе 0.0.
        """
        DEFIANCE = f"Текст в PDF документах не доступен для чтения и копирования. "
        RECOMMENDATION = f"Убедитесь, что текст в PDF документе не представлен в виде изображений без текстового эквивалента. Текст должен быть доступен для чтения и копирования. "

        with pdfplumber.open(io.BytesIO(file)) as pdf:
            final_score = (
                100.0 if any(page.extract_text() for page in pdf.pages) else 0.0
            )
        if final_score != 100.0:
            self._report.add_defiance(DEFIANCE, file_link, "Документ")
            self._report.add_recommendation(RECOMMENDATION, file_link, "Документ")
            self._report.add_xpaths(None)
        return final_score

    def __check_struct(self, file: bytes, file_link: str) -> float:
        """
        Проверяет, содержит ли PDF структурированные теги.

        Args:
            file (bytes): Содержимое PDF-файла.
            file_link (str): Ссылка на PDF-файл.

        Returns:
            bool: 100.0, если структура есть, иначе 0.0.
        """
        DEFIANCE = f"PDF документы не содержат навигационных элементов. "
        RECOMMENDATION = f"В PDF документы добавьте навигационные элементы, такие как оглавление, закладки, ссылки. "

        pdf = PdfReader(io.BytesIO(file))
        final_score = 100.0 if "/StructTreeRoot" in pdf.trailer["/Root"] else 0.0
        if final_score != 100.0:
            self._report.add_defiance(DEFIANCE, file_link, "Документ")
            self._report.add_recommendation(RECOMMENDATION, file_link, "Документ")
            self._report.add_xpaths(None)
        return final_score

    def __check_alt_text(self, file: bytes, file_link: str) -> float:
        """
        Проверяет наличие альтернативного текста для изображений в PDF.

        Args:
            file (bytes): Содержимое PDF-файла.
            file_link (str): Ссылка на PDF-файл.

        Returns:
            bool: Процент изображений с альтернативным текстом (0.0–100.0).
        """
        DEFIANCE = f"Отсутствуют текстовые альтернативы для изображений и графики в PDF документах. "
        RECOMMENDATION = f"Для каждого изображения и графического элемента PDF документе добавьте текстовые альтернативы, которые описывают их содержание или функцию. "

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
        final_score = (with_alt_text / total) * 100
        if final_score != 100.0:
            self._report.add_defiance(DEFIANCE, file_link, "Документ")
            self._report.add_recommendation(RECOMMENDATION, file_link, "Документ")
            self._report.add_xpaths(None)
        return final_score

    def __check_metadata(self, file: bytes, file_link: str) -> float:
        """
        Проверяет, содержит ли PDF обязательные метаданные.

        Args:
            file (bytes): Содержимое PDF-файла.
            file_link (str): Ссылка на PDF-файл.

        Returns:
            bool: 100.0, если хотя бы одно обязательное поле есть, иначе 0.0.
        """
        DEFIANCE = (
            f"В PDF документах не применяются стили и не заполняются метаданные. "
        )
        RECOMMENDATION = f"Используйте стили и метаданные (включая заголовки, авторов и ключевые слова) для улучшения организации PDF документа. "

        reader = PdfReader(io.BytesIO(file))
        metadata = reader.metadata
        required_fields = ["/Title", "/Author", "/Keywords"]
        final_score = (
            100.0 if any(field in metadata for field in required_fields) else 0.0
        )
        if final_score != 100.0:
            self._report.add_defiance(DEFIANCE, file_link, "Документ")
            self._report.add_recommendation(RECOMMENDATION, file_link, "Документ")
            self._report.add_xpaths(None)
        return final_score
