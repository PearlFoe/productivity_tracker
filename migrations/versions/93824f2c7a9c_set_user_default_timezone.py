"""Set user default timezone

Revision ID: 93824f2c7a9c
Revises: 47aa913d9c3c
Create Date: 2025-02-11 12:05:53.488032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93824f2c7a9c'
down_revision: Union[str, None] = '47aa913d9c3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE pt.user SET timezone='Etc/UTC';")
    
    op.alter_column("user", "timezone", nullable=False, server_default="Etc/UTC", schema="pt")


def downgrade() -> None:
    op.alter_column("user", "timezone", nullable=True, server_default=None, schema="pt")
