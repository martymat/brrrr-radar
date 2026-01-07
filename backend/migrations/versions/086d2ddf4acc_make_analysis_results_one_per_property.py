"""make analysis_results one-per-property

Revision ID: 086d2ddf4acc
Revises: 816704c345b6
Create Date: 2026-01-06 08:20:34.560815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '086d2ddf4acc'
down_revision: Union[str, Sequence[str], None] = '816704c345b6'
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