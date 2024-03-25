"""remove username

Revision ID: e0d0f6e50009
Revises: ffb6e4cf57e8
Create Date: 2024-03-25 14:59:19.642184

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e0d0f6e50009"
down_revision: Union[str, None] = "ffb6e4cf57e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "username")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
    )
