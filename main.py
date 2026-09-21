from fastapi import FastAPI
from database import Base, engine
import models
from routes import plantas
from routes import doencas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Verdexa API",
    description="API para identificação e acompanhamento de doenças em plantas.",
    version="1.0.0"
)

app.include_router(plantas.router)
app.include_router(doencas.router)

@app.get("/")
def inicio():

    return {
        "projeto": "Verdexa",
        "status": "API funcionando"
    }