"""empty message

Revision ID: 32ceb64caa4e
Revises: 224609a9ce89
Create Date: 2023-02-12 08:12:40.635062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32ceb64caa4e'
down_revision = '224609a9ce89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venueId', sa.Integer(), nullable=False),
    sa.Column('showId', sa.Integer(), nullable=False),
    sa.Column('Time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'venueId', 'showId')
    )
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=150), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('website_link')

    op.drop_table('Show')
    # ### end Alembic commands ###