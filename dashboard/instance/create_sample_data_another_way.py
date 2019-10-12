from datetime import datetime, timedelta
from time import sleep
from instance.sqliteDB import SqliteDB

sample_data = "create_tables.sql"


def create_sample_data(future_seconds=100, filename=sample_data):
    # future_seconds = 100
    schema = """
    DELETE FROM AIR_QUALITY_INDEX;
    DELETE FROM MAC_NUM;
    DELETE FROM NOISE_INDEX;
    CREATE TABLE IF NOT EXISTS MAC_NUM(
        ID INT PRIMARY KEY, -- integer starting from 1
        MAC_N INT,         
        TIME_NOW DATETIME, -- 精确到秒
        ROOM_NUM TEXT
    );
    
    CREATE TABLE IF NOT EXISTS NOISE_INDEX(
        ID INT PRIMARY KEY, -- integer starting from 1
        NOISE_LEVEL REAL, -- float
        TIME_NOW DATETIME, -- 精确到秒
        ROOM_NUM TEXT
    );
    
    CREATE TABLE IF NOT EXISTS AIR_QUALITY_INDEX(
        ID INT PRIMARY KEY, -- integer starting from 1
        QUALITY_LEVEL REAL, -- float
        TIME_NOW DATETIME, -- 精确到秒
        ROOM_NUM TEXT
    );
    """
    with SqliteDB() as db:
        db.executescript(schema)
        with open(filename, "w") as f:
            f.write(schema)
            time = datetime.now()
            s1 = timedelta(seconds=1)
            for i in range(1, future_seconds):
                t = time + (s1 * i)
                t = t.strftime("%Y-%m-%d %H:%M:%S")
                sql = (
                    f"""INSERT OR REPLACE INTO MAC_NUM(ID, MAC_N, TIME_NOW, ROOM_NUM) VALUES ({i}, {i}, '{t}','{i % 4}');\n""")
                f.write(sql)
                db.executescript(sql)
                # for i in range(1, future_seconds):
                #     t = time + s1 * i
                #     t = t.strftime("%Y-%m-%d %H:%M:%S")
                sql = (
                    f"""INSERT OR REPLACE INTO NOISE_INDEX(ID, NOISE_LEVEL, TIME_NOW,ROOM_NUM) VALUES ({i}, {i + 0.1}, '{t}','{i % 4}');\n""")
                f.write(sql)
                db.executescript(sql)
                # for i in range(1, future_seconds):
                #     t = time + s1 * i
                #     t = t.strftime("%Y-%m-%d %H:%M:%S")
                sql = (
                    f"""INSERT OR REPLACE INTO AIR_QUALITY_INDEX(ID, QUALITY_LEVEL, TIME_NOW,ROOM_NUM) VALUES ({i}, {i + 0.1}, '{t}','{i % 4}');\n""")
                f.write(sql)
                db.executescript(sql)

                sleep(1)


create_sample_data(1000, sample_data)
