"""

Revision ID: 9382847f01c6
Revises: c3582fa18871
Create Date: 2024-11-05 22:37:01.390936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9382847f01c6'
down_revision: Union[str, None] = 'c3582fa18871'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_reward_associations_id', table_name='reward_associations')
    op.drop_table('reward_associations')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reward_associations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('reward_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('target_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('target_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['reward_id'], ['rewards.id'], name='reward_associations_reward_id_fkey', onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='reward_associations_pkey')
    )
    op.create_index('ix_reward_associations_id', 'reward_associations', ['id'], unique=False)
    # ### end Alembic commands ###
