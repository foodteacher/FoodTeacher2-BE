"""modify foreign_key settings

Revision ID: c9d91d089e05
Revises: 69e9c5dc8c33
Create Date: 2024-05-22 18:21:00.275441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9d91d089e05'
down_revision: Union[str, None] = '69e9c5dc8c33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
