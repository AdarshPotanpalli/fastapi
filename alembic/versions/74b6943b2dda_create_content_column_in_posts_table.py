"""create content column in posts table

Revision ID: 74b6943b2dda
Revises: a270d736c7f9
Create Date: 2025-04-20 22:46:22.934727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74b6943b2dda'
down_revision: Union[str, None] = 'a270d736c7f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('posts', 'content')
    pass
