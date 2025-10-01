from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.get_roles_routes import router as roles_router
from routes.get_object_routes import router as objects_router
from routes.get_field_routes import router as fields_router
from routes.get_layouts_routes import router as layouts_router
from routes.get_meta_data import router as meta_router
from routes.get_listing_routes import router as listing_router

app = FastAPI(title="My Python SQL Server App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(roles_router, prefix="/api")
app.include_router(objects_router, prefix="/api")
app.include_router(fields_router, prefix="/api")
app.include_router(layouts_router, prefix="/api")
app.include_router(meta_router, prefix="/api")
app.include_router(listing_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "My Python SQL Server App"}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8001)