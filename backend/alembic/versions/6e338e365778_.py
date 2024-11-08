"""

Revision ID: 6e338e365778
Revises: 337eb693eddf
Create Date: 2024-11-07 05:44:43.132640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e338e365778'
down_revision: Union[str, None] = '337eb693eddf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op


def upgrade():
    # Rimuovi la vecchia chiave primaria da area_conquest_rewards
    op.drop_constraint('area_conquest_rewards_pkey', 'area_conquest_rewards', type_='primary')
    # Aggiungi la nuova chiave primaria
    op.create_primary_key(
        'area_conquest_rewards_pkey',
        'area_conquest_rewards',
        ['reward_type', 'area_conquest_id']
    )

    # Rimuovi la vecchia chiave primaria da species_conquest_rewards
    op.drop_constraint('species_conquest_rewards_pkey', 'species_conquest_rewards', type_='primary')
    # Aggiungi la nuova chiave primaria
    op.create_primary_key(
        'species_conquest_rewards_pkey',
        'species_conquest_rewards',
        ['reward_type', 'species_conquest_id']
    )

    # Rimuovi la vecchia chiave primaria da original_creation_rewards
    op.drop_constraint('original_creation_rewards_pkey', 'original_creation_rewards', type_='primary')
    # Aggiungi la nuova chiave primaria
    op.create_primary_key(
        'original_creation_rewards_pkey',
        'original_creation_rewards',
        ['reward_type', 'original_creation_id']
    )


def downgrade():
    # Ripristina la vecchia chiave primaria per area_conquest_rewards
    op.drop_constraint('area_conquest_rewards_pkey', 'area_conquest_rewards', type_='primary')
    op.create_primary_key(
        'area_conquest_rewards_pkey',
        'area_conquest_rewards',
        ['reward_type', 'item_id', 'area_conquest_id']
    )

    # Ripristina la vecchia chiave primaria per species_conquest_rewards
    op.drop_constraint('species_conquest_rewards_pkey', 'species_conquest_rewards', type_='primary')
    op.create_primary_key(
        'species_conquest_rewards_pkey',
        'species_conquest_rewards',
        ['reward_type', 'item_id', 'species_conquest_id']
    )

    # Ripristina la vecchia chiave primaria per original_creation_rewards
    op.drop_constraint('original_creation_rewards_pkey', 'original_creation_rewards', type_='primary')
    op.create_primary_key(
        'original_creation_rewards_pkey',
        'original_creation_rewards',
        ['reward_type', 'item_id', 'original_creation_id']
    )
