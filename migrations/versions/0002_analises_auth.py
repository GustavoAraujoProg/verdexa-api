"""Campos adicionais; não remove registros nem reinterpreta confiança histórica."""
from alembic import op
import sqlalchemy as sa
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    # A escala antiga não foi documentada. Evita converter percentuais silenciosamente.
    invalidos = bind.execute(sa.text('SELECT COUNT(*) FROM resultados_analise WHERE precisao_ia IS NULL OR precisao_ia < 0 OR precisao_ia > 1')).scalar()
    if invalidos:
        raise RuntimeError('Há confiança histórica nula ou fora de 0..1. Faça backup e normalize os dados conforme README antes de migrar.')
    with op.batch_alter_table('usuarios') as batch:
        batch.add_column(sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()))
    with op.batch_alter_table('analises') as batch:
        batch.add_column(sa.Column('planta_id', sa.Integer(), nullable=True))
        batch.add_column(sa.Column('status', sa.String(30), nullable=False, server_default='pendente'))
        batch.add_column(sa.Column('conclusao', sa.String(40), nullable=True))
        batch.add_column(sa.Column('versao_modelo', sa.String(100), nullable=True))
        batch.add_column(sa.Column('erro', sa.String(255), nullable=True))
        batch.create_foreign_key('fk_analises_planta', 'plantas', ['planta_id'], ['id'])
        batch.create_index('ix_analises_usuario_id', ['usuario_id'])
    bind.execute(sa.text("UPDATE analises SET status = 'legado'"))
    with op.batch_alter_table('resultados_analise') as batch:
        batch.create_check_constraint('ck_confianca', 'precisao_ia >= 0 AND precisao_ia <= 1')
        batch.create_index('ix_resultados_analise_analise_id', ['analise_id'])
    with op.batch_alter_table('historico_cuidados') as batch:
        batch.create_index('ix_historico_cuidados_analise_id', ['analise_id'])


def downgrade():
    raise RuntimeError('Downgrade destrutivo desabilitado; restaure um backup.')
