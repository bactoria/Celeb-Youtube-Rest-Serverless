import os
import psycopg2
import logging
from crawler import crawling

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_name = os.environ['DB_NAME']
# db_port = 5432

# RDS에 연결
conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))


def lambda_handler(event, context):
    try:
        cursor = conn.cursor()

        # SelectAll
        cursor.execute('SELECT * FROM CHANNEL');
        channelIdList = cursor.fetchall()

        for channelId in channelIdList:
            channel = crawling(channelId[0])

            logger.info(channel)

            id = channelId[0]
            title = channel['title']
            content = channel['content']
            image = channel['image']
            joinDate = channel['joinDate']
            subscriber = channel['subscriber']
            views = channel['views']
            updatedTime = channel['updatedTime']

            # PostgreSQL Default Port Number
            sql = 'UPDATE channel SET title=%s, content=%s, subscriber=%s, image=%s, views=%s, join_date=%s, updated_time=%s WHERE id=%s'

            # 쿼리 출력
            logger.info(cursor.mogrify(sql, (title, content, subscriber, image, views, joinDate, updatedTime, id)))

            # 쿼리 실행
            cursor.execute(sql, (title, content, subscriber, image, views, joinDate, updatedTime, id))

            # 커밋
            conn.commit()

    except Exception as e:
        logger.error(e)
