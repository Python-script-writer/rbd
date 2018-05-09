import psycopg2


username = 'postgres'
password = 'qtum_next'
database1 = 'hotel booking'
database2 = 'fly booking'
database3 = 'account'

config1 = {'user': username, 'password': password, 'dbname': database1}
config2 = {'user': username, 'password': password, 'dbname': database2}
config3 = {'user': username, 'password': password, 'dbname': database3}

connect1 = psycopg2.connect(**config1)
cursor1 = connect1.cursor()

connect2 = psycopg2.connect(**config2)
cursor2 = connect2.cursor()

connect3 = psycopg2.connect(**config3)
cursor3 = connect3.cursor()

def create_table_fb():
    #id, client_name, fly_number, place_from, place_to, fly_date
    cursor2.execute(""" CREATE TABLE IF NOT EXISTS fly_booking (
                            id SERIAL PRIMARY KEY,
                            client_name VARCHAR(255) NOT NULL,
                            fly_number INTEGER NOT NULL,
                            place_from VARCHAR(255) NOT NULL,
                            place_to VARCHAR(255) NOT NULL,
                            fly_date INTEGER NOT NULL);
                    """)
    connect2.commit()
    print('fly_booking created')


def create_table_hb():
    #id, client_name, hotel_name, arrival, departure
    cursor1.execute(""" CREATE TABLE IF NOT EXISTS hotel_booking (
                            id SERIAL PRIMARY KEY,
                            client_name VARCHAR(255) NOT NULL,
                            hotel_name VARCHAR(255) NOT NULL,
                            arrival INTEGER NOT NULL,
                            departure INTEGER NOT NULL);
                    """)
    connect1.commit()
    print('fly_booking created')


def make_commit_a():
    cursor3.execute(""" CREATE TABLE IF NOT EXISTS amount (
                            id serial PRIMARY KEY,
                            amountT int check (amountT >= 0));
                    """)
    cursor3.execute("""INSERT INTO amount (amountT)
                        VALUES (%s);
                    """, (100,))
    print('amount created')


create_table_hb()
create_table_fb()
make_commit_a()
try:
    None
except:
    print("Crash DB")
finally:
    cursor1.close()
    cursor2.close()
    cursor3.close()

    connect1.close()
    connect2.close()
    connect3.close()
