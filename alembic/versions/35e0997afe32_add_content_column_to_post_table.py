"""add content column to post table

Revision ID: 35e0997afe32
Revises: 64786413a0e0
Create Date: 2024-12-21 08:59:35.327410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35e0997afe32'
down_revision: Union[str, None] = '64786413a0e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')