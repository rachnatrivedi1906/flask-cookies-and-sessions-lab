"""add is_member_only to articles

Revision ID: 8f1d5d7e2f9a
Revises: 73ea98f39001
Create Date: 2026-06-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f1d5d7e2f9a'
down_revision = '73ea98f39001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('articles', sa.Column('is_member_only', sa.Boolean(), server_default=sa.false(), nullable=False))


def downgrade():
    op.drop_column('articles', 'is_member_only')