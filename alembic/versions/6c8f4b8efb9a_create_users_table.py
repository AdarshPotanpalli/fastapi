"""create users table

Revision ID: 6c8f4b8efb9a
Revises: 74b6943b2dda
Create Date: 2025-04-20 23:03:52.731965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c8f4b8efb9a'
down_revision: Union[str, None] = '74b6943b2dda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable= False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default= sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
