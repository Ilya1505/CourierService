"""Fixed timezone in models

Revision ID: a17ab2cec00d
Revises: d0f27e961dcf
Create Date: 2024-01-15 14:24:19.052347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a17ab2cec00d'
down_revision: Union[str, None] = 'd0f27e961dcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('courier', 'registration_at',
               existing_type=postgresql.TIMESTAMP(timezone=False),
               type_=sa.DateTime(),
               existing_comment='time of registration',
               existing_nullable=False)
    op.drop_constraint('courier_x_district_district_sid_fkey', 'courier_x_district', type_='foreignkey')
    op.drop_constraint('courier_x_district_courier_sid_fkey', 'courier_x_district', type_='foreignkey')
    op.create_foreign_key(None, 'courier_x_district', 'courier', ['courier_sid'], ['sid'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'courier_x_district', 'district', ['district_sid'], ['sid'], source_schema='public', referent_schema='public')
    op.alter_column('order', 'registration_at',
               existing_type=postgresql.TIMESTAMP(timezone=False),
               type_=sa.DateTime(),
               existing_comment='time of registration',
               existing_nullable=False)
    op.drop_constraint('order_district_sid_fkey', 'order', type_='foreignkey')
    op.drop_constraint('order_courier_sid_fkey', 'order', type_='foreignkey')
    op.create_foreign_key(None, 'order', 'courier', ['courier_sid'], ['sid'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'order', 'district', ['district_sid'], ['sid'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'order', schema='public', type_='foreignkey')
    op.create_foreign_key('order_courier_sid_fkey', 'order', 'courier', ['courier_sid'], ['sid'])
    op.create_foreign_key('order_district_sid_fkey', 'order', 'district', ['district_sid'], ['sid'])
    op.alter_column('order', 'registration_at',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_comment='time of registration',
               existing_nullable=False)
    op.drop_constraint(None, 'courier_x_district', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'courier_x_district', schema='public', type_='foreignkey')
    op.create_foreign_key('courier_x_district_courier_sid_fkey', 'courier_x_district', 'courier', ['courier_sid'], ['sid'])
    op.create_foreign_key('courier_x_district_district_sid_fkey', 'courier_x_district', 'district', ['district_sid'], ['sid'])
    op.alter_column('courier', 'registration_at',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_comment='time of registration',
               existing_nullable=False)
    # ### end Alembic commands ###
