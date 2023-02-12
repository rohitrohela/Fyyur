"""empty message

Revision ID: 94af4c89b753
Revises: 32ceb64caa4e
Create Date: 2023-02-12 09:23:37.402421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94af4c89b753'
down_revision = '32ceb64caa4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Show', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artistId', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'Artist', ['artistId'], ['id'])
        batch_op.create_foreign_key(None, 'Venue', ['venueId'], ['id'])
        batch_op.drop_column('showId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Show', schema=None) as batch_op:
        batch_op.add_column(sa.Column('showId', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('artistId')

    # ### end Alembic commands ###