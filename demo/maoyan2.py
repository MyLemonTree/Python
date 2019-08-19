import requests
import json
import pandas as pd

# 爬取哪吒影评
# 创建格式化的url
url = "http://m.maoyan.com/mmdb/comments/movie/1217513.json?_v_=yes&offset={}&startTime=2018-08-{}%2015%3A10%3A31"
date = range(20, 23)


def get_json(url, k_name):
    json_str = requests.get(url=url, headers=headers).content
    data = json.loads(json_str)
    data = data[str(k_name)]
    return data


def mao_yan():
    # 先创建列标题
    df = pd.DataFrame(columns=['city', 'content'])
    print("开始爬取...")
    cnt = 0
    for day in date:
        try:
            for page in range(0, 100):
                url1 = url.format(page * 15, str(day))
                # 最新短评
                data_cmts = get_json(url1, 'cmts')
                # 最热短评
                data_hcmts = get_json(url1, 'hcmts')
                for data_cmt in data_cmts:
                    item = {}
                    if cnt == 0:
                        for data_hcmt in data_hcmts:
                            item['city'] = data_hcmt['cityName']
                            item['content'] = data_hcmt['content']
                            item['date'] = data_hcmt['startTime']
                            # print(data_hcmt['content'])
                            df = df.append(item, ignore_index=True)
                        cnt += 1
                    item['city'] = data_cmt['cityName']
                    item['content'] = data_cmt['content']
                    item['date'] = data_cmt['startTime']
                    df = df.append(item, ignore_index=True)
        except Exception as e:
            # print(e)
            df.to_csv('train_set.csv', encoding='utf_8_sig')
            continue

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'Cookie: v=3; _lxsdk_cuid=16554d073e0c8-0466acea4118ec-37664109-1fa400-16554d073e1c8; __utma=17099173.352741702.1534726616.1534726616.1534726616.1; __utmc=17099173; __utmz=17099173.1534726616.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uuid_n_v=v1; iuuid=05529860A45311E893A585450EFA4776DE80F9A20D504B69A86AC6CD0300BE26; webp=true; ci=51%2C%E5%AE%81%E6%B3%A2; theme=moviepro; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk=05529860A45311E893A585450EFA4776DE80F9A20D504B69A86AC6CD0300BE26; _lxsdk_s=1656479ad1d-6df-fd8-3d3%7C%7C49',
'Host': 'm.maoyan.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

if __name__ == "__main__":
    mao_yan()
    print("爬取已结束。。。")