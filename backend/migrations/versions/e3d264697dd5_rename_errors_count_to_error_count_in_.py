"""rename errors_count to error_count in scrape_runs

Revision ID: e3d264697dd5
Revises: 6e55972aa9bb
Create Date: 2026-01-06 07:57:58.577865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3d264697dd5'
down_revision: Union[str, Sequence[str], None] = '6e55972aa9bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "scrape_runs",
        "errors_count",
        new_column_name="error_count",
    )

def downgrade():
    op.alter_column(
        "scrape_runs",
        "error_count",
        new_column_name="errors_count",
    )