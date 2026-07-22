"""remove_code_column_from_brand

Revision ID: 76c02f446bf1
Revises: 3550d9ef68a2
Create Date: 2026-07-22 12:34:06.312941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76c02f446bf1'
down_revision: Union[str, None] = '3550d9ef68a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drops unique constraint 'uq_brand_company_code' and 'code' column in brand table safely using batch
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.drop_constraint('uq_brand_company_code', type_='unique')
        batch_op.drop_column('code')


def downgrade() -> None:
    # Re-adds the column and unique constraint if downgraded
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.VARCHAR(length=50), nullable=True))
        batch_op.create_unique_constraint('uq_brand_company_code', ['company_id', 'code'])
