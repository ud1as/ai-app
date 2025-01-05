import tempfile
from pathlib import Path
from typing import Optional, Union

from core.rag.extractor.csv_extractor import CSVExtractor
from core.rag.extractor.entity.datasource_type import DatasourceType
from core.rag.extractor.entity.extract_setting import ExtractSetting
from core.rag.extractor.excell_extractor import ExcelExtractor
from core.rag.extractor.extractor_base import BaseExtractor
from core.rag.extractor.html_extractor import HtmlExtractor
from core.rag.extractor.markdown_extractor import MarkdownExtractor
from core.rag.extractor.pdf_extractor import PdfExtractor
from core.rag.extractor.text_extractor import TextExtractor
from core.rag.extractor.word_extractor import WordExtractor
from core.rag.models.document import Document
from core.rag.models.model import UploadFile
from repository.s3_storage import S3Storage


class ExtractProcessor:
    def __init__(self, storage: S3Storage):
        self.storage = storage

    def load_from_upload_file(
        self, upload_file: UploadFile, return_text: bool = False
    ) -> Union[list[Document], str]:
        extract_setting = ExtractSetting(
            datasource_type="upload_file",
            upload_file=upload_file,
            document_model="text_model",
        )

        if return_text:
            delimiter = "\n"
            return delimiter.join(
                [document.page_content for document in self.extract(extract_setting)]
            )
        else:
            return self.extract(extract_setting)

    def extract(
        self, extract_setting: ExtractSetting, file_path: Optional[str] = None
    ) -> list[Document]:
        if extract_setting.datasource_type == DatasourceType.FILE.value:
            with tempfile.TemporaryDirectory() as temp_dir:
                if not file_path:
                    assert (
                        extract_setting.upload_file is not None
                    ), "upload_file is required"
                    upload_file: UploadFile = extract_setting.upload_file
                    suffix = Path(upload_file.key).suffix
                    file_path = (
                        f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"  # type: ignore
                    )

                    self.storage.download(upload_file.key, file_path)

                input_file = Path(file_path)
                file_extension = input_file.suffix.lower()
                extractor: Optional[BaseExtractor] = None

                if file_extension == ".docx":
                    extractor = WordExtractor(file_path)
                elif file_extension == ".pdf":
                    extractor = PdfExtractor(file_path)
                elif file_extension in {".htm", ".html"}:
                    extractor = HtmlExtractor(file_path)
                elif file_extension in {".md", ".markdown", ".mdx"}:
                    extractor = MarkdownExtractor(file_path, autodetect_encoding=True)
                elif file_extension in {".xlsx", ".xls"}:
                    extractor = ExcelExtractor(file_path)
                elif file_extension == ".csv":
                    extractor = CSVExtractor(file_path, autodetect_encoding=True)
                else:
                    # for .txt files
                    extractor = TextExtractor(file_path, autodetect_encoding=True)

                if extractor is None:
                    raise ValueError("No suitable extractor found for the file")

                return extractor.extract()
        else:
            raise ValueError(
                f"Unsupported datasource type: {extract_setting.datasource_type}"
            )
