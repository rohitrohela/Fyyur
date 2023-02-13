"""empty message

Revision ID: cfab47de9f47
Revises: 94af4c89b753
Create Date: 2023-02-12 11:19:28.334822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfab47de9f47'
down_revision = '94af4c89b753'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isLookingForVenues', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seekingDescription', sa.String(), nullable=True))

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isLookingForTalent', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seekingDescription', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('seekingDescription')
        batch_op.drop_column('isLookingForTalent')

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('seekingDescription')
        batch_op.drop_column('isLookingForVenues')

    # ### end Alembic commands ###
