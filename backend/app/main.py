import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router, initialize_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load/build index at startup
    initialize_index()
    yield


app = FastAPI(
    title="IndicSearch Engine API",
    description="Scalable Unicode Text Analytics and Inverted-Index Search Engine for Indian-Language Wikipedia",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to IndicSearch API Engine",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
