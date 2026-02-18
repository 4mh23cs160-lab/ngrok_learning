from fastapi import FastAPI
from routes import user_routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
