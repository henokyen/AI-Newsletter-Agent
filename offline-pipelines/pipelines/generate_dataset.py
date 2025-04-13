from pathlib import Path

from zenml import pipeline

from steps.generate_dataset import create_histograms, generate_summary_dataset
from steps.operations import (
    #push_to_huggingface,
    save_dataset_to_disk,
    retrieve_documents_from_disk
)
from loguru import logger

@pipeline
def generate_dataset(
    load_dataset_id: str,
    summarization_agent_model_id: str = "gpt-4o-mini",
    summarization_agent_mock: bool = False,
    summarization_max_characters: int = 256,
    val_split_ratio: float = 0.1,
    test_split_ratio: float = 0.1,
    min_document_characters: int = 50,
    min_quality_score: float = 0.3,
    augmentation_loops: int = 4,
    max_workers: int = 10,
    data_dir: Path = Path("data/")
) -> None:
    crawled_data_dir = data_dir / "enhanced"
    logger.info(f"Reading notion data from {crawled_data_dir}")
    documents = retrieve_documents_from_disk(
        crawled_data_dir,
        nesting_level=0
    )
    logger.info(f"Generating a histogram ...")
    create_histograms(documents)

    logger.info(f"Performing summurization ...")

    dataset = generate_summary_dataset(
        documents=documents,
        summarization_model=summarization_agent_model_id,
        val_split_ratio=val_split_ratio,
        test_split_ratio=test_split_ratio,
        min_document_characters=min_document_characters,
        min_quality_score=min_quality_score,
        augmentation_loops=augmentation_loops,
        max_workers=max_workers,
        mock=summarization_agent_mock,
        summarization_max_characters=summarization_max_characters,
    )

    save_dataset_to_disk(dataset, 
                         output_dir=data_dir / "instruct_dataset" / load_dataset_id)