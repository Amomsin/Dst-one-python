import asyncio
import sqlite3
import re
from getdata import HttpHelper
import json


async def search_database(pattern):
    # 创建数据库连接
    conn = sqlite3.connect(r'game_data.db')
    cursor = conn.cursor()
    # 使用LIKE进行模糊匹配
    cursor.execute('''
    SELECT * FROM game_info WHERE name LIKE ?
    ''', (f'%{pattern}%',))
    # 获取所有匹配的结果
    rows = cursor.fetchall()
    # 关闭数据库连接
    conn.close()
    return rows


async def search_database_by_id(id):
    config = {
        'DefaultRgion': ['ap-east-1', 'us-east-1', 'eu-central-1', 'ap-southeast-1'],
        'DefaultPlatform': ['Steam', 'Rail', 'WeGame'],
        'Token': 'pds-g^KU_iC59_53i^ByQO7jK+mAPCqmyfQEo5eONht2EL6pCSKjz+1kFA2fI='
    }
    helper = HttpHelper()
    detail_info = await helper.get_detail_info_async(config, id)
    if not detail_info:
        return '未找到匹配的结果'
    # 确保 detail_info 是一个字典
    with open(r'detail_info.json', 'w', encoding='utf-8') as f:
        json.dump(detail_info, f, ensure_ascii=False, indent=4)
    # 读取JSON文件
    with open(r'detail_info.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 格式化数据
    formatted_info = format_main_info(data)
    # print(formatted_info)
    return formatted_info


async def search_main(pattern):
    # print(pattern[:4])
    if pattern[:4] == ' /房间':
        match = re.match(r'^ /房间\s*(.*)', pattern)
        if match:
            pattern = match.group(1).strip()
            # print(pattern)
        else:
            return '请输入正确的查询命令如：\n/查询 [房间名字]\n/房间 [房间id]'
        results = await search_database_by_id(pattern)
        if results:
            return results
        else:
            return '未找到匹配的结果'
    elif pattern[:4] == ' /查询':
        match = re.match(r'^ /查询\s*(.*)', pattern)
        if match:
            pattern = match.group(1).strip()
            # print(pattern)
        else:
            return '请输入正确的查询命令如：\n/查询 [房间名字]\n/房间 [房间id]'
        results = await search_database(pattern)
        if results:
            formatted_results = format_results(results)
            return formatted_results
        else:
            return '未找到匹配的结果'
    else:
        return '请输入正确的查询命令如：\n/查询 [房间名字]\n/房间 [房间id]'


def format_results(results):
    formatted = []
    for row in results:
        formatted.append(
            f"房间名: {row[1]},\n模式: {translate_mode(row[2])}, \n"
            f"房间ID: {row[3]}, "
            f"\n"
            f"季节: {translate_season(row[4])}, "
            f"\n"
            f"已连接/最大连接数: {row[6]}/{row[5]}, "
            f"\n"
            # f"版本: {row[7]}, "
            # f"\n"
            f"平台: {translate_platform(row[8])}"
        )
    return '\n'.join(formatted)


def format_main_info(data):
    main_info = (
        f"房间名: {data.get('name')}\n"
        f"服务器地址: {translate_address(data.get('__addr'))}\n"
        f"模式: {translate_mode(data.get('mode'))}\n"
        f"季节: {translate_season(data.get('season'))}\n"
        f"当前在线玩家数: {data.get('connected')}/{data.get('maxconnections')}\n"
        f"平台: {translate_platform(data.get('platform'))}\n"
        # f"版本: {data.get('v')}\n"
        f"是否专用服务器: {data.get('dedicated')}\n"
        f"玩家信息: \n{format_players(data.get('players'))}\n"
        f"MOD信息: \n{format_mods(data.get('mods_info'))}"
    )
    return main_info


def format_players(players):
    pattern = re.compile(
        r'\{\s*colour="(.*?)",\s*eventlevel=(\d+),\s*name="(.*?)",\s*netid="(.*?)",\s*prefab="(.*?)"\s*\}')
    matches = pattern.findall(players)

    if not matches:
        return "无"

    formatted_players = []
    for index, match in enumerate(matches, start=1):
        colour, eventlevel, name, netid, prefab = match
        formatted_players.append(
            f"{index}:{name}({translate_prefab(prefab)})")
    return '\n'.join(formatted_players)


def format_mods(mods_info):
    formatted_mods = []
    enabled_mods = []
    # 过滤出启用的 MOD
    for i in range(0, len(mods_info), 5):
        mod = mods_info[i:i+5]
        if mod[4]:  # 检查是否启用
            enabled_mods.append(mod)
    # 按顺序标号输出启用的 MOD 信息
    for index, mod in enumerate(enabled_mods, start=1):
        formatted_mods.append(
            f"{index}:{mod[1]}"
        )
    return '\n'.join(formatted_mods)


def translate_address(address):
    if address == '127.0.0.1':
        return '本地服务器无法直连'
    return address


def translate_mode(mode):
    translations = {
        'endless': '无尽',
        'survival': '生存',
        'wilderness': '荒野',
        'relaxed': '放松',
        'oceanfishing': '海钓'
    }
    return translations.get(mode, mode)


def translate_season(season):
    translations = {
        "spring": "春天",
        "summer": "夏天",
        "autumn": "秋天",
        "winter": "冬天"
    }
    return translations.get(season, season)


def translate_platform(platform):
    translations = {
        '1': 'Steam',
        '4': 'WeGame',
        '2': 'PlayStation',
        '19': 'XBone',
        '32': 'Switch'
    }
    return translations.get(str(platform), platform)


def translate_prefab(prefab):
    prefab_translations = {
        'wilson': '威尔逊',
        'willow': '薇洛',
        'wolfgang': '沃尔夫冈',
        'wendy': '温蒂',
        'wickerbottom': '薇克巴顿',
        'woodie': '伍迪',
        'wes': '韦斯',
        'waxwell': '麦斯威尔',
        'wathgrithr': '薇格弗德',
        'webber': '韦伯',
        'winona': '薇诺娜',
        'warly': '沃利',
        'walter': '沃尔特',
        'wortox': '沃拓克斯',
        'wormwood': '沃姆伍德',
        'wurt': '沃特',
        'wanda': '旺达',
        'wonkey': '芜猴',
        'lg_fanglingche': '[海洋传说]方灵澈',
        'lg_lilingyi': '[海洋传说]李令仪',
        'musha': '[精灵公主]穆莎',
    }
    return prefab_translations.get(prefab, prefab)
# # 运行异步任务
# asyncio.run(search_database('lu'))
