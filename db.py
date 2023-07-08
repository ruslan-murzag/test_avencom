import psycopg2

conn = psycopg2.connect(dbname='db_avencom', user='user_avencom', password='', host='localhost')
cursor = conn.cursor()

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