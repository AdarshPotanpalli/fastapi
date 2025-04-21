"""created post table

Revision ID: a270d736c7f9
Revises: 
Create Date: 2025-04-20 21:52:11.981462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a270d736c7f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # create a table
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable= False,
                    primary_key= True), sa.Column('title', sa.String(), nullable= False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    # delete the table
    op.drop_table('posts')
    
    pass
