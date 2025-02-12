"""empty message

Revision ID: 52d9134859c1
Revises: 10dd9d92fd15
Create Date: 2025-02-12 08:19:02.363895

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "52d9134859c1"
down_revision: Union[str, None] = "10dd9d92fd15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("refresh_tokens", "expires_in")


def downgrade() -> None:
    op.add_column(
        "refresh_tokens", sa.Column("expires_in", sa.Integer(), nullable=False)
    )
