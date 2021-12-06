"""empty message

Revision ID: e85381752bc1
Revises: 3a190600d3b9
Create Date: 2021-12-05 15:15:58.501684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e85381752bc1'
down_revision = '3a190600d3b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ads', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ads', 'price')
    # ### end Alembic commands ###
