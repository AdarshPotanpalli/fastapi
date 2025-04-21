"""adding last few columns to post table

Revision ID: 615d708b637e
Revises: fb1a65a54803
Create Date: 2025-04-21 13:46:32.903059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '615d708b637e'
down_revision: Union[str, None] = 'fb1a65a54803'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                                     server_default= "TRUE", nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone= True),
                                     server_default= sa.text('now()'), nullable=False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
