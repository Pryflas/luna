"""initial

Revision ID: 001
Revises:
Create Date: 2025-11-10

"""

from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_buildings_id"), "buildings", ["id"], unique=False)

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.CheckConstraint("level <= 3", name="check_activity_level"),
        sa.ForeignKeyConstraint(["parent_id"], ["activities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_activities_id"), "activities", ["id"], unique=False)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organizations_id"), "organizations", ["id"], unique=False)
    op.create_index(
        op.f("ix_organizations_name"), "organizations", ["name"], unique=False
    )

    op.create_table(
        "phone_numbers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_phone_numbers_id"), "phone_numbers", ["id"], unique=False)

    op.create_table(
        "organization_activity",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], ondelete="CASCADE"
        ),
    )

    # Тестовые данные
    op.execute(
        """
        INSERT INTO buildings (address, latitude, longitude) VALUES
        ('г. Москва, ул. Ленина 1, офис 3', 55.7558, 37.6173),
        ('г. Санкт-Петербург, Невский пр., 28', 59.9343, 30.3351),
        ('г. Новосибирск, ул. Красный пр., 1', 55.0084, 82.9357);
    """
    )

    op.execute(
        """
        INSERT INTO activities (name, parent_id, level) VALUES
        ('Еда', NULL, 1),
        ('Автомобили', NULL, 1);
    """
    )

    op.execute(
        """
        INSERT INTO activities (name, parent_id, level) VALUES
        ('Мясная продукция', 1, 2),
        ('Молочная продукция', 1, 2),
        ('Грузовые', 2, 2),
        ('Легковые', 2, 2);
    """
    )

    op.execute(
        """
        INSERT INTO activities (name, parent_id, level) VALUES
        ('Запчасти', 2, 2),
        ('Аксессуары', 2, 2);
    """
    )

    op.execute(
        """
        INSERT INTO organizations (name, building_id) VALUES
        ('ООО "Рога и Копыта"', 1),
        ('ИП Иванов', 2),
        ('АО "Продукты"', 3);
    """
    )

    op.execute(
        """
        INSERT INTO phone_numbers (number, organization_id) VALUES
        ('2-222-222', 1),
        ('3-333-333', 1),
        ('8-923-666-13-13', 1),
        ('8-800-555-35-35', 2),
        ('8-383-123-45-67', 3);
    """
    )

    op.execute(
        """
        INSERT INTO organization_activity (organization_id, activity_id) VALUES
        (1, 3),
        (1, 4),
        (2, 6),
        (3, 1);
    """
    )


def downgrade():
    op.drop_table("organization_activity")
    op.drop_table("phone_numbers")
    op.drop_table("organizations")
    op.drop_table("activities")
    op.drop_table("buildings")
