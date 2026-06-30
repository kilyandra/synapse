from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models  # noqa: F401
from routers import auth as auth_router
from routers import results as results_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Synapse API",
    docs_url="/api",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router.router)
api_router.include_router(results_router.router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok"}
