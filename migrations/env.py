from alembic import context
from config import settings
from database import Base, engine
import models

if context.is_offline_mode():
    context.configure(url=settings.database_url, target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    with engine.connect() as connection:
        if engine.dialect.name == 'sqlite':
            connection.exec_driver_sql('PRAGMA foreign_keys=OFF')
            connection.commit()
        context.configure(connection=connection, target_metadata=Base.metadata, render_as_batch=engine.dialect.name == 'sqlite')
        with context.begin_transaction():
            context.run_migrations()
        if engine.dialect.name == 'sqlite':
            violations = connection.exec_driver_sql('PRAGMA foreign_key_check').fetchall()
            connection.commit()
            connection.exec_driver_sql('PRAGMA foreign_keys=ON')
            if violations:
                raise RuntimeError('Chaves estrangeiras inválidas após a migração; restaure o backup.')
