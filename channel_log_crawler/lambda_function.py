import os
import psycopg2
from psycopg2.extras import DictCursor
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_name = os.environ['DB_NAME']
# db_port = 5432

# RDS 연결
conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))
cursor = conn.cursor(cursor_factory=DictCursor)


def lambda_handler(event, context):
    try:
        # SelectAll
        cursor.execute('SELECT * FROM channel');
        channelList = cursor.fetchall()

        updated_time = datetime.datetime.now()
        date_time = updated_time.replace(minute=0, second=0, microsecond=0)

        for channel in channelList:
            id = channel['id']
            subscriber = channel['subscriber']

            # PostgreSQL Default Port Number
            sql = '''
            INSERT INTO channel_log("id", "date_time", "updated_time", "subscriber")
            VALUES(%s,%s,%s,%s);
            '''

            # 쿼리 출력
            logger.info(cursor.mogrify(sql, (id, date_time, updated_time, subscriber)))

            # 쿼리 실행
            cursor.execute(sql, (id, date_time, updated_time, subscriber))

        # 커밋
        conn.commit()

    except Exception as e:
        logger.error(e)
        conn.rollback()
