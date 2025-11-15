from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pubmed_pipeline.utils.log_config import get_logger
from pubmed_pipeline.api.routes.ask_routes import router as ask_router
from pubmed_pipeline.api.routes.rag_routes import router as rag_router

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="PubMed RAG API",
        version="1.0.0",
        description="Multi-agent RAG pipeline over PubMed + PGVector + Azure OpenAI.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ask_router, prefix="/api")
    app.include_router(rag_router, prefix="/api")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    logger.info("🚀 FastAPI application initialized.")
    return app


app = create_app()
