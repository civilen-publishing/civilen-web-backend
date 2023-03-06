
from app.api.api import apiRouter
from app.core.config import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    _app = FastAPI(
        title=get_settings().PROJECT_NAME,
        description=get_settings().PROJECT_DESCRIPTION,
        version=get_settings().PROJECT_VERSION,
        docs_url=get_settings().PROJECT_ENVIRONMENT == "development" and "/docs" or None,
        redoc_url=get_settings().PROJECT_ENVIRONMENT == "development" and "/redoc" or None,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @_app.get("/health", include_in_schema=False)
    async def health() -> JSONResponse:
        """Health check endpoint"""
        return JSONResponse(status_code=200, content={"status": "ok"})

    _app.include_router(apiRouter, prefix="/api")

    # Catch all exceptions and return a JSON response
    @_app.exception_handler(Exception)
    async def exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred while processing the request", "status": "error"},
        )

    # mount the upload directory
    _app.mount("/uploads", StaticFiles(directory="/src/uploads"), name="uploads")

    return _app


app = create_app()
