"""Create schedule and report tables

Revision ID: 69e5a0e4377c
Revises: 93824f2c7a9c
Create Date: 2025-02-11 13:06:03.245389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69e5a0e4377c'
down_revision: Union[str, None] = '93824f2c7a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "schedule",
        sa.Column("id", sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("time", sa.Time(), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
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
        sa.ForeignKeyConstraint(["user_id"], ["pt.user.id"], name="fk_schedule_user_id_user_id"),
        schema="pt",
    )

    op.create_table(
        "report",
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("schedule_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
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
        sa.ForeignKeyConstraint(["user_id"], ["pt.user.id"], name="fk_report_user_id_user_id"),
        sa.ForeignKeyConstraint(["schedule_id"], ["pt.schedule.id"], name="fk_report_schedule_id_schedule_id"),
        schema="pt",
    )


def downgrade() -> None:
    op.drop_table("report", schema="pt")
    op.drop_table("schedule", schema="pt")
