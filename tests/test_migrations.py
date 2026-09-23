import os
import subprocess
import sys
from pathlib import Path
from sqlalchemy import create_engine, text, inspect


def alembic(url, *args):
    env = dict(os.environ, DATABASE_URL=url)
    return subprocess.run([sys.executable, '-m', 'alembic', *args], env=env, capture_output=True, text=True)


def test_migracao_com_dados(tmp_path):
    url = 'sqlite:///' + str(tmp_path/'legado.db')
    r = alembic(url, 'upgrade', '0001')
    assert r.returncode == 0, r.stderr
    engine = create_engine(url)
    with engine.begin() as db:
        db.execute(text("INSERT INTO usuarios(id,nome,email,senha_hash) VALUES (1,'Pessoa','pessoa@example.com','hash')"))
        db.execute(text("INSERT INTO plantas(id,nome_popular) VALUES (1,'Tomateiro')"))
        db.execute(text("INSERT INTO doencas(id,planta_id,nome_doenca) VALUES (1,1,'Teste')"))
        db.execute(text("INSERT INTO analises(id,usuario_id,url_imagem) VALUES (1,1,'antiga.jpg')"))
        db.execute(text("INSERT INTO resultados_analise(id,analise_id,doenca_id,precisao_ia) VALUES (1,1,1,.92)"))
        db.execute(text("INSERT INTO historico_cuidados(id,analise_id,observacao,status_planta) VALUES (1,1,'Observação','melhorando')"))
    r = alembic(url, 'upgrade', 'head')
    assert r.returncode == 0, r.stderr
    with engine.connect() as db:
        assert db.execute(text('SELECT status FROM analises')).scalar() == 'legado'
        assert db.execute(text('SELECT precisao_ia FROM resultados_analise')).scalar() == .92
        assert db.execute(text('SELECT COUNT(*) FROM historico_cuidados')).scalar() == 1
        assert not db.execute(text('PRAGMA foreign_key_check')).fetchall()
    assert alembic(url, 'upgrade', 'head').returncode == 0
    engine.dispose()


def test_migracao_banco_novo(tmp_path):
    url = 'sqlite:///' + str(tmp_path/'novo.db')
    r = alembic(url, 'upgrade', 'head')
    assert r.returncode == 0, r.stderr
    engine = create_engine(url)
    assert 'is_admin' in {c['name'] for c in inspect(engine).get_columns('usuarios')}
    engine.dispose()


def test_migracao_bloqueia_escala_ambigua(tmp_path):
    url = 'sqlite:///' + str(tmp_path/'percentual.db')
    assert alembic(url, 'upgrade', '0001').returncode == 0
    engine = create_engine(url)
    with engine.begin() as db:
        db.execute(text('INSERT INTO resultados_analise(analise_id,doenca_id,precisao_ia) VALUES (1,1,92)'))
    r = alembic(url, 'upgrade', 'head')
    assert r.returncode != 0
    assert 'normalize' in r.stderr
    assert 'is_admin' not in {c['name'] for c in inspect(engine).get_columns('usuarios')}
    engine.dispose()
