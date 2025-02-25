"""Add statistics parsing config

Revision ID: 009884f79e7c
Revises: f2c00f3185f7
Create Date: 2025-02-25 15:17:03.340938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009884f79e7c'
down_revision: Union[str, None] = 'f2c00f3185f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "statistics_parsing_config",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("skip_all_day_events", sa.Boolean(), nullable=False, default=True),
        sa.Column("skip_rejected_meetings", sa.Boolean(), nullable=False, default=True),
        sa.Column(
            "created_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('UTC', now())"),
            nullable=False
        ),
        sa.Column(
            "updated_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('UTC', now())"),
            onupdate=sa.text("timezone('UTC', now())"),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_statistics_parsing_config')),
        sa.ForeignKeyConstraint(["user_id"], ["pt.user.id"], name="fk_statistics_parsing_config_user_id_user_id"),
        schema="pt",
    )


def downgrade() -> None:
    op.drop_table("statistics_parsing_config", schema="pt")
