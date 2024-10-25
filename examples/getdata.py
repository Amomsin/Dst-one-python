import requests
import asyncio
import json


class HttpHelper:
    async def get_region_async(self):
        try:
            response = requests.get(
                'https://lobby-v2-cdn.klei.com/regioncapabilities-v2.json')
            result = response.json()
            regions = [x['Region'] for x in result['LobbyRegions']]
            regions.sort(key=lambda x: -1 if x ==
                         'ap-east-1' else (1 if x == 'ap-east-1' else 0))
            return regions
        except Exception as err:
            print('Failed to get Regions:', err)

    async def get_simple_info_by_platform_async(self, config, platform):
        result = []
        try:
            for region in config['DefaultRgion']:
                url = f'https://lobby-v2-cdn.klei.com/{region}-{platform}.json.gz'
                response = requests.get(url)
                print(f'URL: {url}, Status Code: {response.status_code}')
                if response.status_code == 200:
                    try:
                        # print('Response Content:', response.content)
                        result_temp = response.json().get('GET', [])
                        result_temp = [{
                            'name': item.get('name', 'N/A'),
                            'mode': item.get('intent', 'N/A'),
                            'rowId': item.get('__rowId', 'N/A'),
                            'season': item.get('season', 'N/A'),
                            'maxconnections': item.get('maxconnections', 'N/A'),
                            'connected': item.get('connected', 'N/A'),
                            'version': item.get('v', 'N/A'),
                            'platform': item.get('platform', 'N/A')
                        } for item in result_temp]
                    except Exception as error:
                        print('Error processing response:', error)
                        result_temp = []
                    if result_temp:
                        result.extend(result_temp)
            return result
        except Exception as err:
            print('Failed to get SimpleInfo:', err)

    async def get_simple_info_async(self, config):
        result = []
        try:
            for region in config['DefaultRgion']:
                for platform in config['DefaultPlatform']:
                    url = f'https://lobby-v2-cdn.klei.com/{region}-{platform}.json.gz'
                    response = requests.get(url)
                    print(f'URL: {url}, Status Code: {response.status_code}')
                    if response.status_code == 200:
                        try:
                            # print('Response Content:', response.content)
                            result_temp = response.json().get('GET', [])
                            result_temp = [{
                                'name': item.get('name', 'N/A'),
                                'mode': item.get('intent', 'N/A'),
                                'rowId': item.get('__rowId', 'N/A'),
                                'season': item.get('season', 'N/A'),
                                'maxconnections': item.get('maxconnections', 'N/A'),
                                'connected': item.get('connected', 'N/A'),
                                'version': item.get('v', 'N/A'),
                                'platform': item.get('platform', 'N/A')
                            } for item in result_temp]
                        except Exception as error:
                            print('Error processing response:', error)
                            result_temp = []
                        if result_temp:
                            result.extend(result_temp)
            return result
        except Exception as err:
            print('Failed to get SimpleInfo:', err)

    async def get_detail_info_async(self, config, row_id):
        for region in config['DefaultRgion']:
            url = f'https://lobby-v2-{region}.klei.com/lobby/read'
            try:
                payload = {
                    "__token": config['Token'],
                    "__gameId": "DST",
                    "Query": {
                        "__rowId": row_id
                    }
                }
                print(f'POST URL: {url}, Payload: {payload}')
                response = requests.post(url, json=payload)
                print(f'URL: {url}, Status Code: {response.status_code}')
                if response.status_code == 200:
                    try:
                        # print('Response Content:', response.content)
                        return response.json().get('GET', [None])[0]
                    except Exception as error:
                        print('Error processing response:', error)
            except Exception as error:
                print('Error processing response:', error)


# async def main():
#     config = {
#         'DefaultRgion': ['ap-east-1'],
#         'DefaultPlatform': ['Steam', 'Rail'],
#         'Token': 'pds-g^KU_iC59_53i^ByQO7jK+mAPCqmyfQEo5eONht2EL6pCSKjz+1kFA2fI='
#     }
#     helper = HttpHelper()

#     regions = await helper.get_region_async()
#     print('Regions:', regions)

#     simple_info = await helper.get_simple_info_async(config)
    # print('Simple Info:', simple_info)

    # detail_info = await helper.get_detail_info_async(config, id)
    # print('Detail Info:', detail_info)

    # 保存数据到文件
    # with open('simple_info1.json', 'w', encoding='utf-8') as f:
    #     json.dump(simple_info, f, ensure_ascii=False, indent=4)

    # with open('detail_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(detail_info, f, ensure_ascii=False, indent=4)

# asyncio.run(main())
