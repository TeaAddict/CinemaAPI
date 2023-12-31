"""empty message

Revision ID: 3372a35579fb
Revises: 
Create Date: 2023-07-09 16:41:30.167774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3372a35579fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_tags')
    op.drop_table('tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tags_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tags_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('movie_tags',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], name='movie_tags_movie_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='movie_tags_tag_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='movie_tags_pkey')
    )
    # ### end Alembic commands ###
