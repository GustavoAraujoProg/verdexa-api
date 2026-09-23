from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from config import settings
from routes import plantas, doencas, auth, usuarios, analises, cuidados

app = FastAPI(title='Verdexa API', description='Identificação e acompanhamento de doenças em plantas.', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                   allow_credentials=False, allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
                   allow_headers=['Authorization', 'Content-Type'])
for modulo in [plantas, doencas, auth, usuarios, analises, cuidados]:
    app.include_router(modulo.router)


@app.exception_handler(IntegrityError)
async def conflito_integridade(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=409, content={'detail': 'Operação conflita com registros existentes ou vinculados'})


@app.get('/')
def inicio():
    return {'projeto': 'Verdexa', 'status': 'API funcionando', 'ia_configurada': bool(settings.ia_url)}
