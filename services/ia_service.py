from typing import Literal
import httpx
from pydantic import BaseModel, Field, model_validator
from config import settings


class Hipotese(BaseModel):
    doenca_id: int = Field(gt=0)
    confianca: float = Field(ge=0, le=1)


class Predicao(BaseModel):
    versao_modelo: str = Field(min_length=1, max_length=100)
    conclusao: Literal['suspeita_doenca', 'saudavel', 'inconclusivo', 'planta_nao_suportada']
    resultados: list[Hipotese] = Field(default_factory=list, max_length=10)

    @model_validator(mode='after')
    def validar(self):
        if (self.conclusao == 'suspeita_doenca') != bool(self.resultados):
            raise ValueError('Somente suspeita_doenca deve conter hipóteses')
        if len({r.doenca_id for r in self.resultados}) != len(self.resultados):
            raise ValueError('Doenças duplicadas')
        return self


class ServicoIA:
    def analisar(self, caminho, planta_id: int | None) -> Predicao:
        if not settings.ia_url:
            raise RuntimeError('IA não configurada')
        headers = {'Authorization': f'Bearer {settings.ia_api_key}'} if settings.ia_api_key else {}
        with caminho.open('rb') as imagem, httpx.Client(timeout=settings.ia_timeout_seconds) as client:
            response = client.post(settings.ia_url, headers=headers,
                files={'imagem': ('planta.jpg', imagem, 'image/jpeg')},
                data={'planta_id': str(planta_id)} if planta_id else {})
        response.raise_for_status()
        predicao = Predicao.model_validate(response.json())
        if predicao.resultados and max(r.confianca for r in predicao.resultados) < settings.ia_min_confidence:
            predicao.conclusao = 'inconclusivo'
            predicao.resultados = []
        return predicao


def get_ia():
    return ServicoIA()
