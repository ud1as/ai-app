from repository.ext_database import db
from core.rag.models.dataset import Dataset
from typing import List

class DatasetRepository:
    @staticmethod
    def get_datasets_by_tenant(tenant_id: str) -> List[dict]:
        try:
            datasets = db.query(Dataset).filter(Dataset.tenant_id == tenant_id).all()
            return [dataset.to_dict() for dataset in datasets]
        except Exception as e:
            print(f"Error fetching datasets: {e}")
            return []
