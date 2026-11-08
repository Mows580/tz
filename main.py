from fastapi import FastAPI
from src.views.routing.auth import router as auth_router
from src.views.routing.product import router as product_router
from src.views.routing.review import router as review_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(review_router)

if __name__  == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        reload=True
    )