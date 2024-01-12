"""initial migration

Revision ID: 20220115_initial_migration
Revises: 
Create Date: 2024-01-11 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# Use the same DATABASE_URL as in models.py
DATABASE_URL = "sqlite:///./test.db"

# You can use this metadata object or create a new one
metadata = sa.MetaData()

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, index=True),
        sa.Column('email', sa.String, index=True),
        sa.Column('password', sa.String),
    )

def downgrade():
    op.drop_table('users')
