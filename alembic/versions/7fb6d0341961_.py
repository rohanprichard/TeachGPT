"""

Revision ID: 7fb6d0341961
Revises: 
Create Date: 2024-01-18 06:06:47.419353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fb6d0341961'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_table('chat_messages')
    op.drop_index('ix_chats_id', table_name='chats')
    op.drop_index('ix_chats_time', table_name='chats')
    op.drop_table('chats')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.VARCHAR(length=128), nullable=False),
    sa.Column('time', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=128), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_chats_time', 'chats', ['time'], unique=False)
    op.create_index('ix_chats_id', 'chats', ['id'], unique=False)
    op.create_table('chat_messages',
    sa.Column('id', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('chat_id', sa.VARCHAR(length=128), nullable=True),
    sa.Column('message', sa.TEXT(), nullable=True),
    sa.Column('from_user', sa.BOOLEAN(), nullable=True),
    sa.Column('is_opener', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('id', sa.VARCHAR(length=128), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('gender', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('department', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    # ### end Alembic commands ###