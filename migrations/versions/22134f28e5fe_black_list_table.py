"""Black list table.

Revision ID: 22134f28e5fe
Revises: c04e279b0eef
Create Date: 2022-02-22 17:17:59.910064

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "22134f28e5fe"
down_revision = "c04e279b0eef"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "blacklist_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=500), nullable=False),
        sa.Column("blacklisted_on", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("blacklist_tokens")
    # ### end Alembic commands ###
