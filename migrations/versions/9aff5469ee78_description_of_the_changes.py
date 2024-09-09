"""Description of the changes

Revision ID: 9aff5469ee78
Revises: 77dafdda8e2a
Create Date: 2024-09-09 10:36:23.212763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9aff5469ee78'
down_revision = '77dafdda8e2a'
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa

def upgrade():
    # SQLite-specific commands to handle foreign keys
    with op.batch_alter_table('assignment', schema=None) as batch_op:
        # Add the new teacher_id column
        batch_op.add_column(sa.Column('teacher_id', sa.Integer(), nullable=False))

    # Use raw SQL to remove foreign key constraints
    # Since SQLite does not support dropping a specific foreign key by name, 
    # we will rename the table and create a new one
    op.execute('PRAGMA foreign_keys=off;')
    
    # Create a new table with the updated schema
    op.execute('''
    CREATE TABLE new_assignment (
        id INTEGER NOT NULL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        chapter_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        due_date DATETIME,
        file_url VARCHAR(200),
        FOREIGN KEY(chapter_id) REFERENCES chapter (id) ON DELETE CASCADE,
        FOREIGN KEY(teacher_id) REFERENCES user (id) ON DELETE CASCADE
    );
    ''')

    # Copy data from the old table to the new table
    op.execute('''
    INSERT INTO new_assignment (id, title, description, chapter_id, due_date, file_url)
    SELECT id, title, description, chapter_id, due_date, file_url
    FROM assignment;
    ''')

    # Drop the old table
    op.execute('DROP TABLE assignment;')

    # Rename the new table to the original table name
    op.execute('ALTER TABLE new_assignment RENAME TO assignment;')

    op.execute('PRAGMA foreign_keys=on;')  # Re-enable foreign key checks


from alembic import op
import sqlalchemy as sa

def downgrade():
    # SQLite-specific commands to handle foreign keys
    # Use raw SQL to remove foreign key constraints
    # Since SQLite does not support dropping a specific foreign key by name, 
    # we will rename the table and create a new one
    op.execute('PRAGMA foreign_keys=off;')

    # Create a new table with the original schema (before the upgrade)
    op.execute('''
    CREATE TABLE new_assignment (
        id INTEGER NOT NULL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        chapter_id INTEGER NOT NULL,
        student_id INTEGER,
        due_date DATETIME,
        file_url VARCHAR(200),
        FOREIGN KEY(chapter_id) REFERENCES chapter (id) ON DELETE CASCADE,
        FOREIGN KEY(student_id) REFERENCES user (id) ON DELETE CASCADE
    );
    ''')

    # Copy data from the current table to the new table
    op.execute('''
    INSERT INTO new_assignment (id, title, description, chapter_id, due_date, file_url)
    SELECT id, title, description, chapter_id, due_date, file_url
    FROM assignment;
    ''')

    # Drop the current table
    op.execute('DROP TABLE assignment;')

    # Rename the new table back to the original table name
    op.execute('ALTER TABLE new_assignment RENAME TO assignment;')

    op.execute('PRAGMA foreign_keys=on;')  # Re-enable foreign key checks
