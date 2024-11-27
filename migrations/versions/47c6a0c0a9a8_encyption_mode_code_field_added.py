"""Encyption mode code field added.

Revision ID: 47c6a0c0a9a8
Revises: ab0d8e4502a9
Create Date: 2024-11-26 18:01:49.891965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47c6a0c0a9a8'
down_revision = 'ab0d8e4502a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('content', schema=None) as batch_op:
        batch_op.alter_column('encryption_key',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('encrypted_payload',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=10000),
               nullable=False)

    with op.batch_alter_table('device', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('protection_system', schema=None) as batch_op:
        batch_op.add_column(sa.Column('encryption_mode_code', sa.Integer(), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('encryption_mode',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('protection_system', schema=None) as batch_op:
        batch_op.alter_column('encryption_mode',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.drop_column('encryption_mode_code')

    with op.batch_alter_table('device', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('content', schema=None) as batch_op:
        batch_op.alter_column('encrypted_payload',
               existing_type=sa.String(length=10000),
               type_=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('encryption_key',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###