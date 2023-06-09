"""update group

Revision ID: ee280df10699
Revises: 9f8908555781
Create Date: 2023-03-25 21:43:04.930302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee280df10699'
down_revision = '9f8908555781'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'groups', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'groups', type_='unique')
    # ### end Alembic commands ###
