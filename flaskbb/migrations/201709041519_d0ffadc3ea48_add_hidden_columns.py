"""Add hidden columns

Revision ID: d0ffadc3ea48
Revises:
Create Date: 2017-09-04 15:19:38.519991

"""

import sqlalchemy as sa
from alembic import op

import flaskbb

# revision identifiers, used by Alembic.
revision = "d0ffadc3ea48"
down_revision = "881dd22cab94"
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("groups", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("makehidden", sa.Boolean(), nullable=True, default=False)
        )
        batch_op.add_column(
            sa.Column("viewhidden", sa.Boolean(), nullable=True, default=False)
        )

    with op.batch_alter_table("groups", schema=None) as batch_op:
        groups = sa.sql.table(
            "groups",
            sa.sql.column("viewhidden"),
            sa.sql.column("makehidden"),
            sa.sql.column("admin"),
            sa.sql.column("super_mod"),
            sa.sql.column("mod"),
        )
        batch_op.execute(
            groups.update()
            .where(
                sa.or_(
                    groups.c.admin == True,
                    groups.c.mod == True,
                    groups.c.super_mod == True,
                )
            )
            .values(viewhidden=True, makehidden=True)
        )
        batch_op.execute(
            groups.update()
            .where(
                sa.and_(
                    groups.c.admin != True,
                    groups.c.mod != True,
                    groups.c.super_mod != True,
                )
            )
            .values(viewhidden=False, makehidden=False)
        )

        batch_op.alter_column("viewhidden", existing_type=sa.Boolean(), nullable=False)
        batch_op.alter_column("makehidden", existing_type=sa.Boolean(), nullable=False)

    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("hidden", sa.Boolean(), nullable=True, default=False)
        )
        batch_op.add_column(
            sa.Column(
                "hidden_at",
                flaskbb.utils.database.UTCDateTime(timezone=True),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("hidden_by_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_Post_hidden_by", "users", ["hidden_by_id"], ["id"]
        )

    with op.batch_alter_table("posts", schema=None) as batch_op:
        posts = sa.sql.table("posts", sa.sql.column("hidden"))
        batch_op.execute(posts.update().values(hidden=False))
        batch_op.alter_column("hidden", existing_type=sa.Boolean(), nullable=False)

    with op.batch_alter_table("topics", schema=None) as batch_op:
        batch_op.add_column(sa.Column("hidden", sa.Boolean(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "hidden_at",
                flaskbb.utils.database.UTCDateTime(timezone=True),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("hidden_by_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_Topic_hidden_by", "users", ["hidden_by_id"], ["id"]
        )

    with op.batch_alter_table("topics", schema=None) as batch_op:
        topics = sa.sql.table("topics", sa.sql.column("hidden"))
        batch_op.execute(topics.update().values(hidden=False))
        batch_op.alter_column("hidden", existing_type=sa.Boolean(), nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("topics", schema=None) as batch_op:
        batch_op.drop_constraint("fk_Topic_hidden_by", type_="foreignkey")
        batch_op.drop_column("hidden_by_id")
        batch_op.drop_column("hidden_at")
        batch_op.drop_column("hidden")

    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.drop_constraint("fk_Post_hidden_by", type_="foreignkey")
        batch_op.drop_column("hidden_by_id")
        batch_op.drop_column("hidden_at")
        batch_op.drop_column("hidden")

    with op.batch_alter_table("groups", schema=None) as batch_op:
        batch_op.drop_column("viewhidden")
        batch_op.drop_column("makehidden")

    # ### end Alembic commands ###
