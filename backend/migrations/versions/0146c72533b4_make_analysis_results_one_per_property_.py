"""make analysis_results one-per-property v2

Revision ID: 0146c72533b4
Revises: 086d2ddf4acc
Create Date: 2026-01-06 08:21:38.193408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0146c72533b4'
down_revision: Union[str, Sequence[str], None] = '086d2ddf4acc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # enforce one row per property
    op.create_unique_constraint(
        "uq_analysis_results_property_id",
        "analysis_results",
        ["property_id"]
    )

def downgrade():
    op.drop_constraint(
        "uq_analysis_results_property_id",
        "analysis_results",
        type_="unique"
    )