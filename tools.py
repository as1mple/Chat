import argparse

import pymysql


def set_port_key() -> list:
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('-port', '--Port', type=int, help='port', default=3306)
    parser.add_argument('-key', '--Key', type=int, help='key_code', default=2103)
    args = parser.parse_args()
    return [args.Port, args.Key]


def set_port() -> str:
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('-port', '--Port', type=int, help='port', default=3306)
    args = parser.parse_args()
    return args.Port


def add_mysql(table: str, id: int, ip: str, action: str, time: str) -> None:
    connection = pymysql.connect(host='127.0.0.1', user='dev', password='root', db='data', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    mycursor = connection.cursor()

    try:
        sql = "INSERT INTO {} (id, ip, action, time) VALUES (%s, %s, %s, %s)".format(table)
        val = (ip, id, action, time)
        mycursor.execute(sql, val)
        connection.commit()

    except Exception as e:
        print(e)
