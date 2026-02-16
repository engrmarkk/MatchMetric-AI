from pypdf import PdfReader


class PyPDFExtractor:
    def __init__(self, file_obj):
        self.reader = PdfReader(file_obj)

    def extract_text(self) -> str:
        text = ""
        for page in self.reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
