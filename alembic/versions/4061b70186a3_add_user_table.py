"""add user table 

Revision ID: 4061b70186a3
Revises: 35e0997afe32
Create Date: 2024-12-21 09:12:35.165794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4061b70186a3'
down_revision: Union[str, None] = '35e0997afe32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',  
    sa.Column('id', sa.Integer(), nullable=False),  
    sa.Column('email', sa.String(), nullable=False),  
    sa.Column('password', sa.String(), nullable=False),  
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),  
        server_default=sa.text('now()'), nullable=False),  
    sa.PrimaryKeyConstraint('id'),  
    sa.UniqueConstraint('email')  
)  
 

def downgrade() -> None:
    op.drop_table('users')
