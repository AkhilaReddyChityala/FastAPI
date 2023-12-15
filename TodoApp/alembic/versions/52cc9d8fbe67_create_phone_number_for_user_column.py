"""create phone_number for user column

Revision ID: 52cc9d8fbe67
Revises: 
Create Date: 2023-12-14 22:38:13.934802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52cc9d8fbe67'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('Phone_number',sa.String,nulled=True))


def downgrade() -> None:
    op.drop_column('users','Phone_number')
