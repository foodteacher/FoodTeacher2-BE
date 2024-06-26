"""modify user_id field in User

Revision ID: 664dc68d3bc2
Revises: 054e6c9fe50a
Create Date: 2024-05-16 19:30:57.929266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '664dc68d3bc2'
down_revision: Union[str, None] = '054e6c9fe50a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_social_id', sa.String(length=255), nullable=True))
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('users', 'user_social_id')
    # ### end Alembic commands ###
