from datetime import datetime, timedelta

sample_data = "create_tables.sql"


def create_sample_data(future_seconds=100, filename=sample_data):
    # future_seconds = 100
    schema = """
    CREATE TABLE IF NOT EXISTS MAC_NUM(
        ID INT PRIMARY KEY, -- integer starting from 1
        MAC_N INT,         
        TIME_NOW DATETIME -- 精确到秒
    );
    
    CREATE TABLE IF NOT EXISTS NOISE_INDEX(
        ID INT PRIMARY KEY, -- integer starting from 1
        NOISE_LEVEL REAL, -- float
        TIME_NOW DATETIME -- 精确到秒
    );
    
    CREATE TABLE IF NOT EXISTS AIR_QUALITY_INDEX(
        ID INT PRIMARY KEY, -- integer starting from 1
        QUALITY_LEVEL REAL, -- float
        TIME_NOW DATETIME -- 精确到秒
    );
    """

    with open(filename, "w") as f:
        f.write(schema)
        time = datetime.now()
        s1 = timedelta(seconds=1)
        for i in range(1, future_seconds):
            t = time + (s1 * i)
            t = t.strftime("%Y-%m-%d %H:%M:%S")
            sql = ("""INSERT OR REPLACE INTO MAC_NUM(ID, MAC_N, TIME_NOW) VALUES ({}, {}, '{}');\n""".format(i, i, t))
            f.write(sql)
        for i in range(1, future_seconds):
            t = time + s1 * i
            t = t.strftime("%Y-%m-%d %H:%M:%S")
            sql = (
                """INSERT OR REPLACE INTO NOISE_INDEX(ID, NOISE_LEVEL, TIME_NOW) VALUES ({}, {}, '{}');\n""".format(i,
                                                                                                                    i + 0.1,
                                                                                                                    t))
            f.write(sql)

        for i in range(1, future_seconds):
            t = time + s1 * i
            t = t.strftime("%Y-%m-%d %H:%M:%S")
            sql = (
                """INSERT OR REPLACE INTO AIR_QUALITY_INDEX(ID, QUALITY_LEVEL, TIME_NOW) VALUES ({}, {}, '{}');\n""".format(
                    i, i + 0.1, t))
            f.write(sql)


from instance.sqliteDB import SqliteDB

with SqliteDB() as db:
    create_sample_data(100, sample_data)
    db.execute_from_file(sample_data)
