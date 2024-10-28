"""Create separate schema for application

Revision ID: 8e6575ae4499
Revises: 
Create Date: 2024-10-28 14:40:27.979853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e6575ae4499'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA pt")


def downgrade() -> None:
    op.execute("DROP SCHEMA pt")
