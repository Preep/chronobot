import os
import sqlite3


dir_name = os.path.dirname(__file__)

# TODO: Implement query instead of unsafe threading
con = sqlite3.connect(os.path.join(dir_name, 'database.db'), check_same_thread=False)

cur = con.cursor()


def init():
    cur.execute(
        # TODO: Chat_id and user_id are the same. Get rid of one.
        '''
        CREATE TABLE IF NOT EXISTS events (
            user_id INTEGER,
            chat_id INTEGER,
            start_time DATETIME,
            end_time DATETIME,
            text TEXT,
            color TEXT);
        '''
    )
    con.commit()


def add_event(event_dict: dict) -> bool:

    user_id = event_dict['user_id']
    chat_id = event_dict['chat_id']
    start_time = event_dict['start_time']
    end_time = event_dict['end_time']
    text = event_dict['text']
    color = event_dict['color']

    cur.execute(
        '''
        INSERT INTO events (user_id, chat_id, start_time, end_time, text, color)
        VALUES (?, ?, ?, ?, ?, ?);
        ''',
        (user_id, chat_id, start_time, end_time, text, color)
    )
    con.commit()

    # Debug print)))0 00)))
    cur.execute(
        '''
        SELECT * FROM events;
        '''
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    # End of debug print (((((999((
    return True
