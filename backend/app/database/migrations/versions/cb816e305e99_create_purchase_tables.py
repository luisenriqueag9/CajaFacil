"""create_purchase_tables

Revision ID: cb816e305e99
Revises: de4f812d78b9
Create Date: 2026-07-22 22:35:48.517569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb816e305e99'
down_revision: Union[str, None] = 'de4f812d78b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('purchase',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('company_id', sa.UUID(), nullable=False),
        sa.Column('supplier_id', sa.UUID(), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('payment_condition', sa.String(length=20), nullable=False),
        sa.Column('issue_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'supplier_id', 'invoice_number', name='uq_purchase_company_supplier_invoice')
    )
    with op.batch_alter_table('purchase', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_purchase_company_id'), ['company_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_purchase_supplier_id'), ['supplier_id'], unique=False)

    op.create_table('purchase_detail',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('purchase_id', sa.UUID(), nullable=False),
        sa.Column('product_id', sa.UUID(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column('unit_cost', sa.Numeric(precision=18, scale=4), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchase.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('purchase_detail', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_purchase_detail_product_id'), ['product_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_purchase_detail_purchase_id'), ['purchase_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('purchase_detail', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_purchase_detail_purchase_id'))
        batch_op.drop_index(batch_op.f('ix_purchase_detail_product_id'))

    op.drop_table('purchase_detail')

    with op.batch_alter_table('purchase', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_purchase_supplier_id'))
        batch_op.drop_index(batch_op.f('ix_purchase_company_id'))

    op.drop_table('purchase')
