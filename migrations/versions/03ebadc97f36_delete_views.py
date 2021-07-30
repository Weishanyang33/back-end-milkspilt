"""delete views.

Revision ID: 03ebadc97f36
Revises: 51a991bc8b61
Create Date: 2021-07-30 00:07:49.231659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03ebadc97f36'
down_revision = '51a991bc8b61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'view_times')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('view_times', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###