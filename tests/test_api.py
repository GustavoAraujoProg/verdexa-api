import os
import tempfile
from io import BytesIO
from pathlib import Path
os.environ['JWT_SECRET'] = 'segredo-exclusivo-para-testes-com-mais-de-32-caracteres'
os.environ['DATABASE_URL'] = 'sqlite://'
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from config import settings
from database import Base, get_db
from main import app
from models import Usuario, Analise, ResultadoAnalise
from services.ia_service import get_ia, Predicao, ServicoIA


@pytest.fixture()
def ambiente(tmp_path):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    from sqlalchemy import event
    @event.listens_for(engine, 'connect')
    def fk(c, _): c.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    def db():
        with factory() as session:
            try: yield session
            except Exception:
                session.rollback()
                raise
    app.dependency_overrides[get_db] = db
    settings.upload_dir = tmp_path
    settings.ia_url = 'https://modelo.example/predict'
    class IA:
        def analisar(self, caminho, planta_id):
            assert caminho.is_file()
            return Predicao(versao_modelo='teste', conclusao='suspeita_doenca', resultados=[{'doenca_id': 1, 'confianca': 0.92}])
    app.dependency_overrides[get_ia] = IA
    with TestClient(app) as client:
        yield client, factory
    app.dependency_overrides.clear()
    engine.dispose()


def conta(client, email):
    r = client.post('/auth/cadastro', json={'nome': 'Pessoa', 'email': email, 'senha': 'senha-segura123'})
    assert r.status_code == 201
    assert 'senha_hash' not in r.json()
    r = client.post('/auth/login', data={'username': email, 'password': 'senha-segura123'})
    assert r.status_code == 200
    return {'Authorization': 'Bearer ' + r.json()['access_token']}


def imagem():
    buf = BytesIO()
    Image.new('RGB', (64, 64), 'green').save(buf, 'PNG')
    return {'imagem': ('folha.png', buf.getvalue(), 'image/png')}


def catalogo(client, factory):
    admin = conta(client, 'admin@example.com')
    with factory() as db:
        u = db.query(Usuario).filter_by(email='admin@example.com').one()
        u.is_admin = True
        db.commit()
    assert client.post('/plantas/', json={'nome_popular': 'Tomateiro'}, headers=admin).status_code == 200
    assert client.post('/doencas/', json={'planta_id': 1, 'nome_doenca': 'Doença de teste'}, headers=admin).status_code == 200
    return admin


def test_fluxo_e_isolamento(ambiente):
    c, factory = ambiente
    admin = catalogo(c, factory)
    dono = conta(c, 'dono@example.com')
    outro = conta(c, 'outro@example.com')
    assert c.post('/plantas/', json={'nome_popular': 'X'}, headers=dono).status_code == 403
    r = c.post('/analises', files=imagem(), data={'planta_id': 1}, headers=dono)
    assert r.status_code == 201, r.text
    a = r.json()
    assert a['status'] == 'concluida'
    assert a['resultados'][0]['confianca_modelo'] == .92
    url = f"/analises/{a['id']}"
    assert c.get(url+'/imagem', headers=dono).status_code == 200
    for path in [url, url+'/imagem', url+'/cuidados']:
        assert c.get(path, headers=outro).status_code == 404
        assert c.get(path).status_code == 401
    cuidado = {'observacao': 'Folhas novas', 'status_planta': 'melhorando'}
    assert c.post(url+'/cuidados', json=cuidado, headers=outro).status_code == 404
    assert c.post(url+'/cuidados', json=cuidado, headers=dono).status_code == 201
    assert len(c.get(url+'/cuidados', headers=dono).json()) == 1
    assert c.get('/analises', headers=outro).json() == []
    assert c.delete('/doencas/1', headers=admin).status_code == 409
    assert c.delete('/plantas/1', headers=admin).status_code == 409


def test_validacoes(ambiente):
    c, _ = ambiente
    h = conta(c, 'pessoa@example.com')
    assert c.post('/auth/cadastro', json={'nome': 'X', 'email': 'pessoa@example.com', 'senha': 'senha1234'}).status_code == 409
    assert c.post('/auth/login', data={'username': 'pessoa@example.com', 'password': 'errada'}).status_code == 401
    assert c.get('/usuarios/me', headers={'Authorization': 'Bearer invalido'}).status_code == 401
    assert c.patch('/usuarios/me', headers=h, json={'nome': None}).status_code == 422
    assert c.post('/analises', headers=h, files={'imagem': ('falso.jpg', b'nao sou foto', 'image/jpeg')}).status_code == 422
    assert c.post('/analises', headers=h, files={'imagem': ('grande.jpg', b'x'*(11*1024*1024), 'image/jpeg')}).status_code == 413
    assert c.post('/analises', headers=h, files=imagem(), data={'planta_id': 999}).status_code == 404
    settings.ia_url = None
    assert c.post('/analises', headers=h, files=imagem()).status_code == 503
    assert not list(settings.upload_dir.iterdir())


def test_falha_sem_resultado_parcial(ambiente):
    c, factory = ambiente
    h = catalogo(c, factory)
    class Falha:
        def analisar(self, *args):
            return Predicao(versao_modelo='teste', conclusao='suspeita_doenca', resultados=[{'doenca_id': 1, 'confianca': .9}, {'doenca_id': 999, 'confianca': .8}])
    app.dependency_overrides[get_ia] = Falha
    r = c.post('/analises', files=imagem(), headers=h)
    assert r.status_code == 502
    with factory() as db:
        assert db.query(ResultadoAnalise).count() == 0
        assert db.query(Analise).one().status == 'erro'


@pytest.mark.parametrize('conclusao', ['saudavel', 'inconclusivo', 'planta_nao_suportada'])
def test_sem_doenca(ambiente, conclusao):
    c, _ = ambiente
    h = conta(c, 'pessoa@example.com')
    class IA:
        def analisar(self, *args):
            return Predicao(versao_modelo='teste', conclusao=conclusao)
    app.dependency_overrides[get_ia] = IA
    r = c.post('/analises', files=imagem(), headers=h)
    assert r.status_code == 201
    assert r.json()['conclusao'] == conclusao
    assert r.json()['resultados'] == []


def test_adapter_baixa_confianca(ambiente, monkeypatch, tmp_path):
    import httpx
    caminho = tmp_path/'foto.jpg'
    caminho.write_bytes(b'teste')
    def handler(request):
        assert request.method == 'POST'
        return httpx.Response(200, json={'versao_modelo': 'v1', 'conclusao': 'suspeita_doenca', 'resultados': [{'doenca_id': 1, 'confianca': .4}]})
    client = httpx.Client
    monkeypatch.setattr(httpx, 'Client', lambda **kw: client(transport=httpx.MockTransport(handler), **kw))
    r = ServicoIA().analisar(caminho, 1)
    assert r.conclusao == 'inconclusivo'
    assert not r.resultados
