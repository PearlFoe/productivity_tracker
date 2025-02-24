"""Add calendar.disabled flag

Revision ID: f2c00f3185f7
Revises: 69e5a0e4377c
Create Date: 2025-02-24 12:54:38.536251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2c00f3185f7'
down_revision: Union[str, None] = '69e5a0e4377c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("calendar", sa.Column("disabled", sa.DateTime(timezone=True), nullable=True), schema="pt")


def downgrade() -> None:
    op.drop_column("calendar", "disabled", schema="pt")
