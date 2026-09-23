import argparse
from sqlalchemy import update
from database import SessionLocal
from models import Usuario

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('acao', choices=['promover-admin'])
    parser.add_argument('email')
    args = parser.parse_args()
    with SessionLocal() as db:
        result = db.execute(update(Usuario).where(Usuario.email == args.email.lower()).values(is_admin=True))
        if result.rowcount != 1:
            raise SystemExit('Usuário não encontrado. Cadastre a conta primeiro.')
        db.commit()
    print('Administrador atualizado.')
