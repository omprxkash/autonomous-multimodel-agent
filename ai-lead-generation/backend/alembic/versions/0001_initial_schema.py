"""initial schema

Revision ID: 0001
Revises:
Create Date: 2025-07-01 10:00:00.000000

"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company", sa.String(), nullable=False),
        sa.Column("domain", sa.String(), nullable=False, unique=True),
        sa.Column("industry", sa.String()),
        sa.Column("employee_count", sa.Integer()),
        sa.Column("location", sa.String()),
        sa.Column("contact_name", sa.String()),
        sa.Column("title", sa.String()),
        sa.Column("email", sa.String()),
        sa.Column("tech_stack", postgresql.JSONB()),
        sa.Column("score", sa.Integer()),
        sa.Column("score_breakdown", postgresql.JSONB()),
        sa.Column("email_draft", sa.Text()),
        sa.Column("stage", sa.String(), server_default="new"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )
    op.create_table(
        "email_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("email_templates")
    op.drop_table("leads")

