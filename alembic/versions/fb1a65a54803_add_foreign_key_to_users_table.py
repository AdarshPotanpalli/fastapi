"""add foreign key to users table

Revision ID: fb1a65a54803
Revises: 6c8f4b8efb9a
Create Date: 2025-04-20 23:22:02.558523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb1a65a54803'
down_revision: Union[str, None] = '6c8f4b8efb9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table= "posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], 
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fkey', "posts")
    op.drop_column("posts", "owner_id")
    pass
