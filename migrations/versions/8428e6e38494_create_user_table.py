"""Create user table

Revision ID: 8428e6e38494
Revises: 8e6575ae4499
Create Date: 2024-10-28 14:41:28.531238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8428e6e38494'
down_revision: Union[str, None] = '8e6575ae4499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('telegram_id', sa.Integer(), nullable=True),
        sa.Column('timezone', sa.Text, nullable=True),
        sa.Column(
            'created_dt',
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('UTC', now())"),
            nullable=False
        ),
        sa.Column(
            'updated_dt',
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('UTC', now())"),
            onupdate=sa.text("timezone('UTC', now())"),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
        schema='pt'
    )


def downgrade() -> None:
    op.drop_table('user', schema='pt')
