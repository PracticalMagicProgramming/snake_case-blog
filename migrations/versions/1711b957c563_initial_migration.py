"""Initial migration.

Revision ID: 1711b957c563
Revises: 
Create Date: 2022-05-06 16:40:14.649761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1711b957c563'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('pfp_url', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
