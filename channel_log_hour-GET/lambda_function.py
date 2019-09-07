import os
import json
import psycopg2
from psycopg2.extras import DictCursor
import datetime

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_name = os.environ['DB_NAME']

conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))
# RDS 연결
cursor = conn.cursor(cursor_factory=DictCursor)

LOG_COUNT = 7;
KST = datetime.timezone(datetime.timedelta(hours=9))


def lambda_handler(event, context):
    # TODO implement

    id = event['params']['path']['id']
    print(id)

    sql = '''
    SELECT * 
    FROM channel_log
    WHERE id=%s
    ORDER BY date_time desc
    LIMIT %s
    '''

    cursor.execute(sql, (id, LOG_COUNT))
    rows = cursor.fetchall()

    response = []

    for row in rows:
        date_time = row['date_time'].astimezone(tz=KST)

        response.append({
            'id': row['id'],
            'date': date_time.strftime('%Y-%m-%d'),
            'hour': int(date_time.strftime('%H')),
            'subscriber': row['subscriber']
        })

    return response


