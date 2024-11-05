"""Create calendar tables

Revision ID: 05467af3bb95
Revises: 8428e6e38494
Create Date: 2024-10-31 13:04:10.524365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05467af3bb95'
down_revision: Union[str, None] = '8428e6e38494'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'calendar_category',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.TEXT(), nullable=False),
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
        sa.PrimaryKeyConstraint('id', name=op.f('pk_calendar_category')),
        schema='pt',
    )
    
    op.create_table(
        'calendar',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('category', sa.UUID, nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('timezone', sa.Text, nullable=False),
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
        sa.PrimaryKeyConstraint('id', name=op.f('pk_calendar')),
        sa.ForeignKeyConstraint(["category"], ["pt.calendar_category.id"], name="fk_calendar_category_calendar_category"),
        schema='pt',
    )


def downgrade() -> None:
    op.drop_table('calendar', schema='pt')
    op.drop_table('calendar_category', schema='pt')

