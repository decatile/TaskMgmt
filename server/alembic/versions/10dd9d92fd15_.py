"""empty message

Revision ID: 10dd9d92fd15
Revises: f0041b36d1b4
Create Date: 2025-02-11 18:17:22.791826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "10dd9d92fd15"
down_revision: Union[str, None] = "f0041b36d1b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(255), nullable=False))
    op.alter_column("users", "username", type_=sa.String(length=64), nullable=False)


def downgrade() -> None:
    op.drop_column("users", "email")
    op.alter_column("users", "username", type_=sa.String(length=255), nullable=False)
