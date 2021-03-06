"""add username and avatar to question and answer model.

Revision ID: 00f66e49b32e
Revises: 06c9955908d2
Create Date: 2021-08-09 22:19:47.631512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f66e49b32e'
down_revision = '06c9955908d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('username', sa.String(), nullable=True))
    op.add_column('answer', sa.Column('avatar', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'answer', ['username'])
    op.add_column('question', sa.Column('username', sa.String(), nullable=True))
    op.add_column('question', sa.Column('avatar', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'question', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='unique')
    op.drop_column('question', 'avatar')
    op.drop_column('question', 'username')
    op.drop_constraint(None, 'answer', type_='unique')
    op.drop_column('answer', 'avatar')
    op.drop_column('answer', 'username')
    # ### end Alembic commands ###
