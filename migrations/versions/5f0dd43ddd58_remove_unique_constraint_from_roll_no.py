"""Remove unique constraint from Roll_No

Revision ID: 5f0dd43ddd58
Revises: 426d7f94deab
Create Date: 2026-07-29 23:33:17.664030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f0dd43ddd58'
down_revision = '426d7f94deab'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student_db', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('user_id', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            None,
            'user',
            ['user_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('student_db', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')
        batch_op.create_unique_constraint(
            'Roll_No',
            ['Roll_No']
        )