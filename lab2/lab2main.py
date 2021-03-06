import psycopg2
import datetime

username = 'postgres'
password = 'qtum_next'
database1 = 'hotel_booking'
database2 = 'fly_booking'
database3 = 'account'
port = "5432"


def insert_records_2pc(client_name, place_from, place_to, hotel):
    tran_id = "insert"
    id_user = 1542
    fly_conn = psycopg2.connect(database=database1, user=username, password=password, port=port)
    print("Opened databases {}".format(database1))
    hotel_conn = psycopg2.connect(database=database2, user=username, password=password, port=port)
    print("Opened databases {}".format(database2))
    amount_conn = psycopg2.connect(database=database3, user=username, password=password, port=port)
    print("Opened databases {}".format(database3))

    fly_xid = fly_conn.xid(42, tran_id, 'conn1')
    hotel_xid = hotel_conn.xid(42, tran_id, 'conn2')
    amount_xid = amount_conn.xid(42, tran_id, 'conn3')

    fly_conn.tpc_begin(fly_xid)
    hotel_conn.tpc_begin(hotel_xid)
    amount_conn.tpc_begin(amount_xid)

    hotel_cur = hotel_conn.cursor()
    fly_cur = fly_conn.cursor()
    amount_cur = amount_conn.cursor()

    print("Start execute")

    try:

        fly_cur.execute(""" CREATE TABLE IF NOT EXISTS fly_booking (
                            id SERIAL PRIMARY KEY,
                            client_name VARCHAR(255) NOT NULL,
                            fly_number INTEGER NOT NULL,
                            place_from VARCHAR(255) NOT NULL,
                            place_to VARCHAR(255) NOT NULL,
                            fly_date INTEGER NOT NULL);
                        """)

        fly_cur.execute(
            """INSERT INTO fly_booking (id, client_name, fly_number, place_from, place_to, fly_date)
            VALUES (%s, %s, 32, %s, %s, 13 )""", (id_user, client_name, place_from, place_to))

        hotel_cur.execute(""" CREATE TABLE IF NOT EXISTS hotel_booking (
                            id SERIAL PRIMARY KEY,
                            client_name VARCHAR(255) NOT NULL,
                            hotel_name VARCHAR(255) NOT NULL,
                            arrival INTEGER NOT NULL,
                            departure INTEGER NOT NULL);
                    """)

        hotel_cur.execute(
            """INSERT INTO hotel_booking (id, client_name, hotel_name, arrival, departure)
            VALUES (%s, %s, %s, 11, 13 )""", (id_user, client_name, hotel))

        amount_cur.execute("""SELECT amountT FROM {table} WHERE id=1;""".format(table='amount'))
        someValue = 10
        data = amount_cur.fetchone()
        curr_amount = data[0]
        print("Current amount:", curr_amount, )
        new_am = curr_amount - someValue
        amount_cur.execute("UPDATE amount SET amountT = (%s) WHERE id = (%s);", (new_am, 1))
        print("New amount:", new_am)
        fly_cur.close()
        hotel_cur.close()
        amount_cur.close()

        print("Start prepare")
        fly_conn.tpc_prepare()
        hotel_conn.tpc_prepare()
        amount_conn.tpc_prepare()
        print("All prepared")

    except psycopg2.IntegrityError:
        print("Fail")
        fly_conn.tpc_rollback()
        hotel_conn.tpc_rollback()
        amount_conn.tpc_rollback()
        print("All rollbacked")
    else:

        fly_conn.tpc_commit()
        hotel_conn.tpc_commit()
        amount_conn.tpc_commit()
        print("All commited")
    fly_conn.close()
    hotel_conn.close()
    amount_conn.close()


insert_records_2pc('Name', 'K', 'P', 'I')
