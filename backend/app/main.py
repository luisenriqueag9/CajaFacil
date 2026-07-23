from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import logger
from app.common.exceptions import CajaFacilException
from app.common.responses import APIErrorResponse, BaseAPIResponse
from app.modules.company.presentation.routers.company_router import router as company_router
from app.modules.brand.presentation.routers.brand_router import router as brand_router
from app.modules.category.presentation.routers.category_router import router as category_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan management for startup and shutdown procedures.
    """
    logger.info(f"Starting {settings.APP_NAME} in environment: {settings.ENV}")
    # Startup triggers (e.g. ensuring DB engines connect, establishing caches)
    yield
    # Shutdown triggers (e.g. cleaning pools, closing connections)
    logger.info(f"Shutting down {settings.APP_NAME}")

app = FastAPI(
    title=settings.APP_NAME,
    description="Professional POS SaaS Backend supporting PostgreSQL (Cloud Sync) and SQLite (Offline Mode).",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS configuration to allow Flutter desktop/web client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Exception Handler for CajaFacilException
@app.exception_handler(CajaFacilException)
async def cajafacil_exception_handler(request: Request, exc: CajaFacilException):
    logger.warning(f"Domain error at {request.url.path}: {exc.message} (code: {exc.code})")
    error_payload = APIErrorResponse(
        success=False,
        error_code=exc.code,
        message=exc.message,
        details=exc.details
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload.model_dump()
    )

# Generic fallback Exception Handler for uncaught exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Uncaught system exception at {request.url.path}: {str(exc)}", exc_info=True)
    error_payload = APIErrorResponse(
        success=False,
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected system error occurred. Please contact support.",
        details=str(exc) if settings.DEBUG else None
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload.model_dump()
    )

@app.get("/health", response_model=BaseAPIResponse, tags=["Health"])
async def health_check():
    """
    API Health check endpoint.
    """
    return BaseAPIResponse(
        success=True,
        message="CajaFácil Core API is healthy and operational."
    )

app.include_router(
    company_router,
    prefix="/api/v1/companies",
    tags=["Companies"],
)

app.include_router(
    brand_router,
    prefix="/api/v1/brands",
    tags=["Brands"],
)

app.include_router(
    category_router,
    prefix="/api/v1/categories",
    tags=["Categories"],
)
# Note: Register modular routers here
# Example:
# from app.modules.product.presentation.routes import router as product_router
# app.include_router(product_router, prefix="/api/v1/products", tags=["Product"])
