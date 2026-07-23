"""alter_category_table_remove_code_parent_description_add_protected

Revision ID: 23a39407d1ce
Revises: 76c02f446bf1
Create Date: 2026-07-22 21:32:05.563015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23a39407d1ce'
down_revision: Union[str, None] = '76c02f446bf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safely alter category table using batch for SQLite compatibility
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('protected', sa.Boolean(), nullable=False, server_default=sa.text('0')))
        batch_op.drop_constraint('uq_category_company_code', type_='unique')
        batch_op.drop_constraint('fk_category_parent', type_='foreignkey')
        batch_op.drop_column('code')
        batch_op.drop_column('parent_id')
        batch_op.drop_column('description')


def downgrade() -> None:
    # Downgrade re-adds dropped columns and constraints
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('parent_id', sa.UUID(), nullable=True))
        batch_op.add_column(sa.Column('code', sa.String(length=50), nullable=True))
        batch_op.create_foreign_key('fk_category_parent', 'category', ['parent_id'], ['id'], ondelete='RESTRICT')
        batch_op.create_unique_constraint('uq_category_company_code', ['company_id', 'code'])
        batch_op.drop_column('protected')
