"""add missing order_details columns

Revision ID: 6b7c8d9e0f1a
Revises: 5715af044c39
Create Date: 2025-12-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7c8d9e0f1a'
down_revision = '5715af044c39'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to order_details table if they don't exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('order_details')]
    
    with op.batch_alter_table('order_details', schema=None) as batch_op:
        if 'tracking_number' not in columns:
            batch_op.add_column(sa.Column('tracking_number', sa.String(length=100), nullable=True))
        if 'payment_method' not in columns:
            batch_op.add_column(sa.Column('payment_method', sa.String(length=50), nullable=True, server_default='Cash on Delivery'))
        if 'notes' not in columns:
            batch_op.add_column(sa.Column('notes', sa.Text(), nullable=True))


def downgrade():
    # Remove the columns if downgrading
    with op.batch_alter_table('order_details', schema=None) as batch_op:
        batch_op.drop_column('notes')
        batch_op.drop_column('payment_method')
        batch_op.drop_column('tracking_number')
