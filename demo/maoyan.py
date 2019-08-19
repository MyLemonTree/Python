import requests
import json
import pandas as pd

# 爬取哪吒影评
# 创建格式化的url
url = "http://m.maoyan.com/review/v2/comments.json?movieId=1211270&userId=-1&offset={}&limit=15&ts=1566196804997&type=3"
date = range(20, 21)


def get_json(url, k_name):
    json_str = requests.get(url=url, headers=headers).content
    data = json.loads(json_str)
    data = data['data'][str(k_name)]
    return data


def mao_yan():
    # 先创建列标题
    df = pd.DataFrame(columns=['city', 'content'])
    print("开始爬取...")
    cnt = 0
    for day in date:
        try:
            for page in range(0, 100):
                url1 = url.format(page * 15)
                # 最新短评
                data_cmts = get_json(url1, 'comments')
                # 最热短评
                data_hcmts = get_json(url1, 'hotComments')
                for data_cmt in data_cmts:
                    item = {}
                    if cnt == 0:
                        for data_hcmt in data_hcmts:
                            item['content'] = data_hcmt['content']
                            item['date'] = data_hcmt['startTime']
                            df = df.append(item, ignore_index=True)
                        cnt += 1
                    item['content'] = data_cmt['content']
                    item['date'] = data_cmt['startTime']
                    df = df.append(item, ignore_index=True)
                print(df)
        except Exception as e:
            print(e)
        df.to_csv('train_set3.csv', encoding='utf_8_sig')
        continue

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16ca791aa2ec8-05437c8983afa2-414f0320-100200-16ca791aa2fc8; __mta=142022541.1566179437243.1566179437243.1566179437243.1; uuid_n_v=v1; iuuid=CB962750C22311E98960B5E0473545E60622B8CF96F24319B597E391AF11EE7A; webp=true; ci=50%2C%E6%9D%AD%E5%B7%9E; _lxsdk=CB962750C22311E98960B5E0473545E60622B8CF96F24319B597E391AF11EE7A',
    'Host': 'm.maoyan.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

if __name__ == "__main__":
    mao_yan()
    print("爬取已结束。。。")