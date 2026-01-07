"""add max_results to scrape_runs

Revision ID: 9f64a81022f7
Revises: e3d264697dd5
Create Date: 2026-01-06 08:01:48.803426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f64a81022f7'
down_revision: Union[str, Sequence[str], None] = 'e3d264697dd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("scrape_runs", sa.Column("max_results", sa.Integer(), nullable=False, server_default="50"))
    op.alter_column("scrape_runs", "max_results", server_default=None)

def downgrade():
    op.drop_column("scrape_runs", "max_results")