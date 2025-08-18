from fastapi import FastAPI
from app.routes import expense_routes, category_router, report_router

app = FastAPI(
    title="AgroControl API",
    description="API to manage agricultural expenses (yuca farm tracking)",
    version="1.0.0"
)

app.include_router(expense_routes.router)
app.include_router(category_router.router)
app.include_router(report_router.router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to AgroControl API"}
