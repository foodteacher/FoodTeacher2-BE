"""add refresh_token column in User

Revision ID: 43a4cb2c1e3a
Revises: b012c9cea376
Create Date: 2024-05-22 19:03:02.307975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43a4cb2c1e3a'
down_revision: Union[str, None] = 'b012c9cea376'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('jwt_refresh_token', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'jwt_refresh_token')
