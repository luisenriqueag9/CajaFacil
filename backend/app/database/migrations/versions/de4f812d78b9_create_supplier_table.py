"""create_supplier_table

Revision ID: de4f812d78b9
Revises: 23a39407d1ce
Create Date: 2026-07-22 22:00:49.661174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de4f812d78b9'
down_revision: Union[str, None] = '23a39407d1ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('supplier',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('company_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('tax_id', sa.String(length=50), nullable=True),
        sa.Column('contact_name', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'tax_id', name='uq_supplier_company_tax_id')
    )
    with op.batch_alter_table('supplier', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_supplier_company_id'), ['company_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('supplier', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_supplier_company_id'))

    op.drop_table('supplier')
