include ../../.env


docker:
	docker run -d \
	--name agno-postgres \
	-e POSTGRES_DB=ai \
	-e POSTGRES_USER=ai \
	-e POSTGRES_PASSWORD=ai \
	-p 5532:5432 \
	pgvector/pgvector:pg17


run:
	uv run hitl_confirmation.py