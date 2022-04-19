"""empty message

Revision ID: f912af8449dd
Revises: 4756d9a5befc
Create Date: 2022-03-23 16:52:40.221586

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f912af8449dd"
down_revision = "4756d9a5befc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.add_column(
        "users", sa.Column("last_login_date", sa.DateTime(timezone=True), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "last_login_date")
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###
