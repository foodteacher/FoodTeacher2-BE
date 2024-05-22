"""modify column in User

Revision ID: b012c9cea376
Revises: c9d91d089e05
Create Date: 2024-05-22 18:46:38.504676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b012c9cea376'
down_revision: Union[str, None] = 'c9d91d089e05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'user_id')
    op.add_column('users', sa.Column('user_social_id', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'user_social_id')
    op.add_column('users', sa.Column('user_id', sa.String(length=255), nullable=True))
    # Rename back the user_social_id column to user_id
