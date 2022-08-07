import pymysql
from automation.common.singleton import Singleton
from automation.common.configuration import Configuration


class Database(Singleton):
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(
            host=host, 
            user=user, 
            password=password, 
            database=database,
            charset='utf8',
            autocommit=True
        )
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.db.close()

    def execute_query(self, sql):
        results = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            print('Error: unable to fetch data')
        return results


if __name__ == "__main__":
    db = Database(**Configuration.db_config)
    # sql1 = "select * from `tb_boss` where real_name = '崔'"
    sql1 = "select * from `tb_designer_data`"
    results = db.execute_query(sql1)
    print(results)
    