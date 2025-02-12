"""empty message

Revision ID: 3cc36718d8e3
Revises: 52d9134859c1
Create Date: 2025-02-12 15:36:54.053237

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3cc36718d8e3"
down_revision: Union[str, None] = "52d9134859c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("enabled", sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "enabled")
