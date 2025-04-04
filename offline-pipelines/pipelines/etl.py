from pathlib import Path
from loguru import logger

from zenml import pipeline, step
from steps.operations import (
    retrieve_documents_from_disk,
    save_documents_to_disk
)

from steps.enrichers import (
    crawl,
    grade_document_quality
)

@pipeline
def etl(
        data_dir: Path,
        max_workers : int = 10,
        quality_agent_model_id: str = "gpt-4o-mini",
        quality_agent_mock: bool = True,
) -> None:
   
    notion_data_dir = data_dir/ "notion"
    crawled_data_dir = data_dir / "enhanced"
    logger.info(f"Reading notion data from {notion_data_dir}")

    logger.info(f"Reading json files from {notion_data_dir}")
    documents = retrieve_documents_from_disk(notion_data_dir,
                               nesting_level=1)
    
    logger.info(f"Started crawling ...")
  
    crawled_documents = crawl(documents=documents, max_workers=max_workers)
    enhanced_documents = grade_document_quality(
        documents=crawled_documents,
        model_id=quality_agent_model_id,
        mock=quality_agent_mock,
        max_workers=max_workers,
    )
    save_documents_to_disk(documents=enhanced_documents, 
                           output_dir=crawled_data_dir
                           )