"""Add status column to videos table

Revision ID: b0deff199383
Revises: e9282bdefc3d
Create Date: 2024-01-17 18:08:46.546227

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "b0deff199383"
down_revision: Union[str, None] = "e9282bdefc3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "videos",
        sa.Column(
            "status",
            sa.String(length=255),
            nullable=True,
            default=sa.Text("NOT_PROCESSED"),
        ),
    )


def downgrade() -> None:
    op.drop_column("videos", "status")
