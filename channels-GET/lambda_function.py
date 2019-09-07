import json
import os
import psycopg2
import datetime
from psycopg2.extras import DictCursor
from calculate_subscriber import calculate_subscriber_string

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_name = os.environ['DB_NAME']
# db_port = 5432

# RDS에 연결
conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))
cursor = conn.cursor(cursor_factory=DictCursor)


def lambda_handler(event, context):
    try:
        cursor.execute('''
        SELECT * 
        FROM CHANNEL 
        ORDER BY subscriber desc
        ''');

        resultset = cursor.fetchall()

        result = []

        for row in resultset:
            result.append(
                {
                    'id': row['id'],
                    'name': row['name'],
                    'title': row['title'],
                    'image': row['image'],
                    'subscriber_string': calculate_subscriber_string(row['subscriber'])
                }
            )

        return result

    except Exception as e:
        logger.error(e)


def json_default(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    raise TypeError('not JSON serializable')
