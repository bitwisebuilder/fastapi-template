"""Add file column to videos table

Revision ID: e9282bdefc3d
Revises: d7c04eaeddff
Create Date: 2024-01-17 16:55:37.666243

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "e9282bdefc3d"
down_revision: Union[str, None] = "d7c04eaeddff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("videos", sa.Column("file", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("videos", "file")
