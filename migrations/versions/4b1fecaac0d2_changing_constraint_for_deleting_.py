"""Changing Constraint for Deleting Classroom

Revision ID: 4b1fecaac0d2
Revises: 1c251f2c3d35
Create Date: 2024-09-05 21:42:01.874296

"""
from alembic import op
import sqlalchemy as sa

revision = '4b1fecaac0d2'
down_revision = '1c251f2c3d35'
branch_labels = None
depends_on = None

"""Change the Classroom and Assignment Table

Revision ID: 1c251f2c3d35
Revises: 
Create Date: 2024-09-05 21:35:09.199500

"""
from alembic import op
import sqlalchemy as sa

fk_assignment_student_id_user_id = "fk_assignment_student_id_user_id"
fk_classroom_teacher_id_user_id = "fk_classroom_teacher_id_user_id"
uq_classroom_class_code = "uq_classroom_class_code"

revision = '1c251f2c3d35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('assignment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(fk_assignment_student_id_user_id, 'user', ['student_id'], ['id'])

    with op.batch_alter_table('classroom', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.create_unique_constraint(uq_classroom_class_code, ['class_code'])
        batch_op.create_foreign_key(fk_classroom_teacher_id_user_id, 'user', ['teacher_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('username',
               existing_type=sa.TEXT(),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.TEXT(),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.TEXT(),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.TEXT(),
               type_=sa.String(length=30),
               existing_nullable=False)



def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=30),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=200),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('classroom', schema=None) as batch_op:
        batch_op.drop_constraint(fk_classroom_teacher_id_user_id, type_='foreignkey')
        batch_op.drop_constraint(uq_classroom_class_code, type_='unique')
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('assignment', schema=None) as batch_op:
        batch_op.drop_constraint(fk_assignment_student_id_user_id, type_='foreignkey')
        batch_op.drop_column('student_id')


def upgrade():
    with op.batch_alter_table('assignment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_assignment_classroom_id_classroom', type_='foreignkey')
        batch_op.drop_constraint('fk_assignment_student_id_user_id', type_='foreignkey')

        batch_op.create_foreign_key('fk_assignment_classroom_id_classroom', 'classroom', ['classroom_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_assignment_student_id_user_id', 'user', ['student_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('classroom', schema=None) as batch_op:
        batch_op.drop_constraint('fk_classroom_teacher_id_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_classroom_teacher_id_user_id', 'user', ['teacher_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.drop_constraint('fk_material_classroom_id_classroom', type_='foreignkey')
        batch_op.create_foreign_key('fk_material_classroom_id_classroom', 'classroom', ['classroom_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.drop_constraint('fk_submission_student_id_user_id', type_='foreignkey')
        batch_op.drop_constraint('fk_submission_assignment_id_assignment', type_='foreignkey')

        batch_op.create_foreign_key('fk_submission_student_id_user_id', 'user', ['student_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_submission_assignment_id_assignment', 'assignment', ['assignment_id'], ['id'], ondelete='CASCADE')



def downgrade():
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.drop_constraint('fk_submission_student_id_user_id', type_='foreignkey')
        batch_op.drop_constraint('fk_submission_assignment_id_assignment', type_='foreignkey')

        batch_op.create_foreign_key('fk_submission_student_id_user_id', 'user', ['student_id'], ['id'])
        batch_op.create_foreign_key('fk_submission_assignment_id_assignment', 'assignment', ['assignment_id'], ['id'])

    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.drop_constraint('fk_material_classroom_id_classroom', type_='foreignkey')
        batch_op.create_foreign_key('fk_material_classroom_id_classroom', 'classroom', ['classroom_id'], ['id'])

    with op.batch_alter_table('classroom', schema=None) as batch_op:
        batch_op.drop_constraint('fk_classroom_teacher_id_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_classroom_teacher_id_user_id', 'user', ['teacher_id'], ['id'])

    with op.batch_alter_table('assignment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_assignment_classroom_id_classroom', type_='foreignkey')
        batch_op.drop_constraint('fk_assignment_student_id_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_assignment_classroom_id_classroom', 'classroom', ['classroom_id'], ['id'])
        batch_op.create_foreign_key('fk_assignment_student_id_user_id', 'user', ['student_id'], ['id'])

