"""Add exchange_rates

Revision ID: 38cbfb5b3aa1
Revises: 5108e9db5198
Create Date: 2024-08-07 21:28:31.573934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38cbfb5b3aa1'
down_revision: Union[str, None] = '5108e9db5198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('base_currency_id', sa.Integer(), nullable=False),
    sa.Column('target_currency_id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['base_currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['target_currency_id'], ['currencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exchange_rates')
    # ### end Alembic commands ###
