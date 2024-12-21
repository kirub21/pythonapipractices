"""add last few columns to post table

Revision ID: 0a99373ad70d
Revises: dbd210ec44af
Create Date: 2024-12-21 13:04:17.448473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a99373ad70d'
down_revision: Union[str, None] = 'dbd210ec44af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():  
    op.add_column('posts', sa.Column(  
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),  
    )  
    op.add_column('posts', sa.Column(  
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),  
    )  
    pass

def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
