"""create users table

Revision ID: ffb6e4cf57e8
Revises: b0deff199383
Create Date: 2024-03-24 21:57:42.300843

"""
import datetime
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

# revision identifiers, used by Alembic.
revision: str = "ffb6e4cf57e8"
down_revision: Union[str, None] = "b0deff199383"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        Column("id", Integer, primary_key=True),
        Column("first_name", String(50), nullable=False),
        Column("last_name", String(50), nullable=False),
        Column("username", String(50), nullable=False, unique=True),
        Column("email", String(100), nullable=False, unique=True),
        Column("password", String(200), nullable=False),
        Column("is_active", Boolean, default=True),
        Column("is_superuser", Boolean, default=False),
        Column("created_at", DateTime, default=datetime.datetime.now),
        Column(
            "updated_at",
            DateTime,
            default=datetime.datetime.now,
            onupdate=datetime.datetime.now,
        ),
    )


def downgrade():
    op.drop_table("users")
