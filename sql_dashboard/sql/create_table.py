import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error
import os
import sys
sys.path.append(os.path.abspath(os.path.join('data')))
sys.path.append(os.path.abspath(os.path.join('sql_dashboard/sql')))


def DBConnect(dbName=None):
    conn = mysql.connect(host='localhost', user='root', password='abel6464',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur


def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()


def createDB(dbName: str) -> None:
    conn, cur = DBConnect()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    conn.commit()
    cur.close()


def createTables(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    sqlFile = 'sql_dashboard/sql/database.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')
    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:

    conn, cur = DBConnect(dbName)
    for _, row in df.iterrows():

        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, original_text, retweet_text, sentiment, polarity, 
                    subjectivity, lang, statuses_count, favorite_count, retweet_count, screen_name, followers_count, 
                    friends_count, possibly_sensitive, hashtags, user_mentions, location)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14], row[15], row[16], row[17])

        try:
            cur.execute(sqlQuery, data)
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return


if __name__ == "__main__":
    createDB(dbName='tweet_db')
    emojiDB(dbName='tweet_db')
    createTables(dbName='tweet_db')
    df = pd.read_csv('data/cleaned_economic_data.csv')
    df.info()
    insert_to_tweet_table(dbName='tweet_db', df=df,
                          table_name='tweets')
