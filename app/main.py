from fastapi import FastAPI
from .routes import organizations_router, buildings_router, activities_router
from .database import engine, Base

app = FastAPI(
    title="Organization API",
    description="API для справочника организаций, зданий и видов деятельности",
    version="1.0.0",
)

app.include_router(organizations_router)
app.include_router(buildings_router)
app.include_router(activities_router)


@app.get("/")
def root():
    return {
        "message": "Organization API работает. Документация доступна по адресу /docs"
    }
