import psycopg2


def connect_sql(db_name, user_name, password, host):
    conn = psycopg2.connect(dbname=db_name, user=user_name, password=password, host=host)
    cursor = conn.cursor()
    return conn, cursor


def make_command(conn, cursor):

    commands = (
        """
    CREATE TABLE model (
        id SERIAL PRIMARY KEY , 
        model VARCHAR(255) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE brand (
        id SERIAL PRIMARY KEY , 
        brand VARCHAR(255) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE auto (
        id SERIAL PRIMARY KEY ,
        model INT REFERENCES model (id),
        brand INT REFERENCES model (id),
        price INT,
        year  INT
    )
    """)

    for command in commands:
        cursor.execute(command)

    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    conn, cursor = connect_sql('db_avencom', 'user_avencom', '', 'localhost')
    make_command(conn, cursor)