"""age column change to birthday

Revision ID: 8bd0f6bb0ad3
Revises: b99c70a6a423
Create Date: 2024-05-15 15:21:34.766662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8bd0f6bb0ad3'
down_revision: Union[str, None] = 'b99c70a6a423'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birthday', sa.Date(), nullable=True))
    op.drop_column('users', 'age')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('age', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('users', 'birthday')
    # ### end Alembic commands ###