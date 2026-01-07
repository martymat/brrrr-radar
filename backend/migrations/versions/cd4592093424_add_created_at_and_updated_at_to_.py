"""add created_at and updated_at to analysis_results

Revision ID: cd4592093424
Revises: 0146c72533b4
Create Date: 2026-01-06 08:32:14.272358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd4592093424'
down_revision: Union[str, Sequence[str], None] = '0146c72533b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "analysis_results",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "analysis_results",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # Optional: drop server_default so future inserts rely on app/onupdate behavior
    op.alter_column("analysis_results", "created_at", server_default=None)
    op.alter_column("analysis_results", "updated_at", server_default=None)

def downgrade():
    op.drop_column("analysis_results", "updated_at")
    op.drop_column("analysis_results", "created_at")
