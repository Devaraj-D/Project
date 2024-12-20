"""new column added

Revision ID: ca58891a0258
Revises: 86a667b339be
Create Date: 2024-12-10 03:13:31.077982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca58891a0258'
down_revision = '86a667b339be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_logo', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_column('company_logo')

    # ### end Alembic commands ###
