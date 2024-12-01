from datetime import datetime
from io import BytesIO

from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


DOCUMENT_TITLE = (
    "Отчет проверки доступности веб-сайта для пользователей с нарушением зрения"
)
DEFIANCES_PARAGRAPH = "Выявленные нарушения:"
RECOMMENDATIONS_PARAGRAPH = "Рекомендации:"
FONT_NAME = "Times New Roman"
FONT_SIZE = Pt(16)


class Report:
    def __init__(self, url: str):
        self.__doc = Document()
        self.__url = url
        self.__defiances = []
        self.__recommendations = []

        self.__init_style()
        self.__init_header()

    def __init_style(self):
        style = self.__doc.styles["Normal"]
        style.font.name = FONT_NAME
        style.font.size = FONT_SIZE

    def __init_header(self):
        heading = self.__doc.add_paragraph(DOCUMENT_TITLE)
        heading.runs[0].font.color.rgb = RGBColor(0, 0, 0)
        heading.runs[0].font.bold = True
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        date = datetime.now().strftime("%d.%m.%Y")
        # Страница сайта, дата проверки
        self.__doc.add_paragraph(f"Дата проверки: {date}")
        self.__doc.add_paragraph(f"Страница сайта: {self.__url}")

    def add_defiance(self, text: str) -> None:
        self.__defiances.append(text)

    def add_recommendation(self, text: str) -> None:
        self.__recommendations.append(text)

    def render(self) -> BytesIO:
        v = self.__doc.add_paragraph(DEFIANCES_PARAGRAPH)
        v.runs[0].font.bold = True

        for i, defiance in enumerate(self.__defiances, start=1):
            self.__doc.add_paragraph(f"{i}. {defiance}")

        r = self.__doc.add_paragraph(RECOMMENDATIONS_PARAGRAPH)
        r.runs[0].font.bold = True
        for i, recommendation in enumerate(self.__recommendations, start=1):
            self.__doc.add_paragraph(f"{i}. {recommendation}")

        file = BytesIO()
        self.__doc.save(file)
        file.seek(0)
        return file
