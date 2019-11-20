from typing import Dict, IO, Optional

from pdfminer import converter, pdfdocument, pdfinterp, pdfpage, pdfparser
from pdfminer.layout import LTTextContainer, LAParams

from .components import PDFDocument, Page


def load_file(path_to_file: str, **kwargs) -> PDFDocument:
    with open(path_to_file, "rb") as in_file:
        return load(in_file, pdf_file_path=path_to_file, **kwargs)


def load(
    pdf_file: IO,
    pdf_file_path: Optional[str] = None,
    la_params: Optional[Dict[str, str]] = None,
    **kwargs
) -> PDFDocument:
    if la_params is None:
        la_params = {}

    parser = pdfparser.PDFParser(pdf_file)
    document = pdfdocument.PDFDocument(parser)

    if not document.is_extractable:
        raise pdfpage.PDFTextExtractionNotAllowed

    resource_manager = pdfinterp.PDFResourceManager()
    device = converter.PDFPageAggregator(
        resource_manager, laparams=LAParams(**la_params)
    )
    interpreter = pdfinterp.PDFPageInterpreter(resource_manager, device)

    pages: Dict[int, Page] = {}
    for page in pdfpage.PDFPage.create_pages(document):
        interpreter.process_page(page)
        results = device.get_result()

        page_number = results.pageid

        elements = [
            element for element in results if isinstance(element, LTTextContainer)
        ]

        pages[page_number] = Page(
            width=results.width, height=results.height, elements=elements
        )

    return PDFDocument(pages=pages, pdf_file_path=pdf_file_path, **kwargs)
