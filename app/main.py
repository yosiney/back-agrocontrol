from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import expense_routes, category_router, report_router, project_router

app = FastAPI(
    title="AgroControl API",
    description="API to manage agricultural expenses (yuca farm tracking)",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde cualquier origen (desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Content-Type, Authorization, etc.
)

app.include_router(expense_routes.router)
app.include_router(category_router.router)
app.include_router(report_router.router)
app.include_router(project_router.router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to AgroControl API"}