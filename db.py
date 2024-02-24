from config import db_name, db_password, db_user, host

import psycopg2


def addMessage(user_id, user_name, text='', photo_id='', caption=''):

    executer = f'''INSERT INTO messages (userid, username, messagetext, photoid, caption) VALUES 
    ('{user_id}', '{user_name}', '{text}', '{photo_id}', '{caption}')'''

    try:
        with psycopg2.connect(host=host, user=db_user, password=db_password, database=db_name) as conn:
            with conn.cursor() as curs:
                curs.execute(executer)


    except Exception as _e:
        print('Error:', _e)



