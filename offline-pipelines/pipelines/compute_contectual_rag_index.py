from steps.operations import retrieve_documents_from_disk
from steps.compute_rag_vector_index import filter_by_quality,chunk_embed_load
from loguru import logger
from zenml import pipeline
from pathlib import Path

from commons.rag import EmbeddingModelType
from commons.rag.retrievers import RetrieverType
from commons.rag.splitters import SummarizationType

@pipeline
def compute_rag_vector_index(
    data_dir: Path,
    extract_collection_name: str,
    fetch_limit: int,
    load_collection_name: str,
    content_quality_score_threshold: float,
    retriever_type: RetrieverType,
    embedding_model_id: str,
    embedding_model_type: EmbeddingModelType,
    embedding_model_dim: int,
    chunk_size: int,
    contextual_summarization_type: SummarizationType = "none",
    contextual_agent_model_id: str | None = None,
    contextual_agent_max_characters: int | None = None,
    mock: bool = False,
    processing_batch_size: int = 256,
    processing_max_workers: int = 10,
    device: str = "cpu",
) -> None:
    crawled_data_dir = data_dir / "enhanced"
    logger.info(f"Reading notion data from {crawled_data_dir}")
    documents = retrieve_documents_from_disk(
        crawled_data_dir,
        nesting_level=0
    )
   
    documents = filter_by_quality(
        documents=documents,
        content_quality_score_threshold=content_quality_score_threshold,
    ) 
    
    chunk_embed_load(
        documents=documents,
        collection_name=load_collection_name,
        processing_batch_size=processing_batch_size,
        processing_max_workers=processing_max_workers,
        retriever_type=retriever_type,
        embedding_model_id=embedding_model_id,
        embedding_model_type=embedding_model_type,
        embedding_model_dim=embedding_model_dim,
        chunk_size=chunk_size,
        contextual_summarization_type=contextual_summarization_type,
        contextual_agent_model_id=contextual_agent_model_id,
        contextual_agent_max_characters=contextual_agent_max_characters,
        mock=mock,
        device=device,
    )