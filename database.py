import oracledb


DB_USER = "studentapp"
DB_PASSWORD = "studentapp123"
DB_DSN = "localhost:1521/XEPDB1"


def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


def test_connection():
    try:
        connection = get_connection()

        print("Oracle database connected successfully!")

        connection.close()

    except Exception as e:
        print("Database connection failed!")
        print(e)


if __name__ == "__main__":
    test_connection()