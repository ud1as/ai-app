from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.rag.models.model import UploadFile


class ExtractSetting(BaseModel):
    """
    Model class for provider response.
    """

    datasource_type: str
    upload_file: Optional[UploadFile] = None
    # notion_info: Optional[NotionInfo] = None
    # website_info: Optional[WebsiteInfo] = None
    document_model: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data) -> None:
        super().__init__(**data)
