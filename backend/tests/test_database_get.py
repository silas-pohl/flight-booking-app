from app import main


def test_database_get():
    database_open = main.database()
    assert(database_open == {"data": "Opened database successfully"})
