export PYTHONPATH = .

# --- Default Values ---

CHECK_DIRS := .
RETRIEVER_CONFIG ?= configs/compute_rag_vector_index_openai_contextual_simple.yaml

# --- Utilities ---

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

check-config:
	@if [ ! -f "$(RETRIEVER_CONFIG)" ]; then \
		echo "Error: Retriever config file '$(RETRIEVER_CONFIG)' does not exist"; \
		exit 1; \
	else \
		echo "Found retriever config file at '$(RETRIEVER_CONFIG)'"; \
	fi

# --- Run ---

run_agent_app: check-config
	@python -m tools.app --retriever-config-path=$(RETRIEVER_CONFIG) --ui

run_agent_query: check-config
	@python -m tools.app --retriever-config-path=$(RETRIEVER_CONFIG) --query "What's the difference between small and large Language models?"

evaluate_agent: check-config
	@python -m tools.evaluate_app --retriever-config-path=$(RETRIEVER_CONFIG)