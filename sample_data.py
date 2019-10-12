from datetime import datetime, timedelta

future_seconds = 100
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

with open("create_tables.sql", "w") as f:
    f.write(schema)
    time = datetime.now()
    s1 = timedelta(seconds=1)
    for i in range(1, future_seconds):
        t = time + (s1 * i)
        t = t.strftime("%Y-%m-%d %H:%M:%S")
        sql = (f"""INSERT OR REPLACE INTO MAC_NUM(ID, MAC_N, TIME_NOW) VALUES ({i}, {i}, '{t}');\n""")
        f.write(sql)
    for i in range(1, future_seconds):
        t = time + s1 * i
        t = t.strftime("%Y-%m-%d %H:%M:%S")
        sql = (f"""INSERT OR REPLACE INTO NOISE_INDEX(ID, NOISE_LEVEL, TIME_NOW) VALUES ({i}, {i+0.1}, '{t}');\n""")
        f.write(sql)

    for i in range(1, future_seconds):
        t = time + s1 * i
        t = t.strftime("%Y-%m-%d %H:%M:%S")
        sql = (f"""INSERT OR REPLACE INTO AIR_QUALITY_INDEX(ID, QUALITY_LEVEL, TIME_NOW) VALUES ({i}, {i+0.1}, '{t}');\n""")
        f.write(sql)
