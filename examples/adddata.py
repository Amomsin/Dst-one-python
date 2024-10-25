import sqlite3
import json
import asyncio
from getdata import HttpHelper


async def update_database():
    config = {
        'DefaultRgion': ['ap-east-1', 'us-east-1', 'eu-central-1', 'ap-southeast-1'],
        'DefaultPlatform': ['Steam', 'Rail', 'WeGame'],
        'Token': 'pds-g^KU_iC59_53i^ByQO7jK+mAPCqmyfQEo5eONht2EL6pCSKjz+1kFA2fI='
    }
    helper = HttpHelper()
    simple_info = await helper.get_simple_info_async(config)
    with open(r'simple_info.json', 'w', encoding='utf-8') as f:
        json.dump(simple_info, f, ensure_ascii=False, indent=4)
        
    try:
        # 创建数据库连接
        conn = sqlite3.connect(r'game_data.db')
        cursor = conn.cursor()

        # 删除现有表（如果存在）
        cursor.execute('DROP TABLE IF EXISTS game_info')

        # 创建新表
        cursor.execute('''
        CREATE TABLE game_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mode TEXT,
            rowId TEXT,
            season TEXT,
            maxconnections INTEGER,
            connected INTEGER,
            version INTEGER,
            platform INTEGER
        )
        ''')

        # 读取JSON文件
        with open(r'simple_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 插入数据
        for item in data:
            cursor.execute('''
            INSERT INTO game_info (name, mode, rowId, season, maxconnections, connected, version, platform)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item['name'], item['mode'], item['rowId'], item['season'], item['maxconnections'], item['connected'], item['version'], item['platform']))

        # 提交事务
        conn.commit()

        print("数据库已根据JSON文件更新")

    except sqlite3.Error as e:
        print(f"数据库操作错误: {e}")

    finally:
        # 关闭数据库连接
        if conn:
            conn.close()


# # 无限循环，每5分钟执行一次
# while True:
#     update_database()
#     # 等待5分钟（300秒）
#     time.sleep(300)
# asyncio.run(update_database())
