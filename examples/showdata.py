import sqlite3


async def show_database():
    # 创建数据库连接
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    # 执行查询
    cursor.execute('SELECT * FROM game_info')

    # 获取所有结果
    rows = cursor.fetchall()

    # 打印结果
    for row in rows:
        print(row)

    # 关闭数据库连接
    conn.close()
