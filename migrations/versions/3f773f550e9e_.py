"""empty message

Revision ID: 3f773f550e9e
Revises: 
Create Date: 2023-10-25 15:32:42.082101

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3f773f550e9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('target_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    # ### end Alembic commands ###
