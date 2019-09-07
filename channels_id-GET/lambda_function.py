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


def lambda_handler(event, context):
    # TODO implement

    id = event['params']['path']['id']
    print(id)
    sql = "SELECT * FROM CHANNEL WHERE id=%s"

    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    print(dict(row))

    response = {
        'id': id,
        'name': row['name'],
        'introVideoUrl': row['intro_video_url'],
        'title': row['title'],
        'content': row['content'],
        'image': row['image'],
        'subscriber': row['subscriber'],
        'joinDate': row['join_date'].strftime('%Y-%m-%d'),
        'views': row['views'],
        'updatedTime': row['updated_time'].isoformat(sep='T', timespec='milliseconds')
    }

    return response