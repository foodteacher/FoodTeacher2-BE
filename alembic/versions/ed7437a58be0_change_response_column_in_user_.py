"""change response column in user_responses to answer

Revision ID: ed7437a58be0
Revises: 43a4cb2c1e3a
Create Date: 2024-05-23 21:12:50.021170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed7437a58be0"
down_revision: Union[str, None] = "43a4cb2c1e3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('user_responses', 'user_answers')
    op.alter_column(
        "user_answers",
        "response",
        new_column_name="answer",
        existing_type=sa.String(255),
        nullable=True,
    )


def downgrade() -> None:
    op.rename_table("user_answers", "user_responses")
    op.alter_column(
        "user_answers",
        "answer",
        new_column_name="response",
        existing_type=sa.String(255),
        nullable=True,
    )
