from app.database import initialize_database, get_connection


def test_database_initialization():
    initialize_database()

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
        """)

        tables = {row[0] for row in cursor.fetchall()}

    assert "accounts" in tables
    assert "transactions" in tables


if __name__ == "__main__":
    test_database_initialization()
    print("✅ Database test passed!")