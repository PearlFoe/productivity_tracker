"""Create statistics table

Revision ID: 47aa913d9c3c
Revises: 05467af3bb95
Create Date: 2024-11-27 19:54:37.561124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47aa913d9c3c'
down_revision: Union[str, None] = '05467af3bb95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'statistics',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('calendar_id', sa.UUID, nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('minutes', sa.Integer, nullable=False),
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
        sa.PrimaryKeyConstraint('id', name=op.f('pk_statistics')),
        sa.ForeignKeyConstraint(["calendar_id"], ["pt.calendar.id"], name="fk_statistics_calendar_id_calendar_id"),
        schema='pt',
    )



def downgrade() -> None:
    op.drop_table('statistics', schema='pt')

