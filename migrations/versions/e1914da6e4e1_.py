"""empty message

Revision ID: e1914da6e4e1
Revises: e85381752bc1
Create Date: 2021-12-05 16:07:38.347469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1914da6e4e1'
down_revision = 'e85381752bc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ads', sa.Column('is_paid', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ads', 'is_paid')
    # ### end Alembic commands ###