"""Added m2m forumgroups table

Revision ID: 127be3fb000
Revises: 514ca0a3282c
Create Date: 2015-04-08 22:25:52.809557

"""

# revision identifiers, used by Alembic.
revision = '127be3fb000'
down_revision = '514ca0a3282c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forumgroups',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['forum_id'], ['forums.id'], name='fk_forum_id', use_alter=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('forumgroups')
    ### end Alembic commands ###