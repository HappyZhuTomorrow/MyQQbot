import requests
import json
import sys
import execjs

class Translate:
    def __init__(self,query):
        self.query = query
        self.url_langdetect = 'https://fanyi.baidu.com/langdetect'
        self.url_trans = 'https://fanyi.baidu.com/v2transapi'
        self.head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            
        }


    def run_js(self):

        #query = 'Hello spider'
        with open('D:\\VSCode-c\\python_project\\baidu_translate_js.js', 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())

        sign = ctx.call('e', self.query)
        return sign
    
    def parse_url(self,url,data,cookie):
        r = requests.post(url,data=data,headers=self.head,cookies=cookie)
        return json.loads(r.content.decode())

    def get_Transresult(url,dict_ret):
        
        dit = dict_ret['trans_result']['data'][0]['dst']
        print(dit)
    
    def run(self):
        lang_derect_data = {"query": self.query}
        cookie_trans={
            'Cookie': 'BIDUPSID=2368B76DB55E7B4FEE7A663ABACC0E4D; PSTM=1635161349; BAIDUID=2368B76DB55E7B4F2296F3879CE79102:FG=1; __yjs_duid=1_dc16c041a1fcac8aca74bdf2d71d8a4c1635172396343; FANYI_WORD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; USERTOKEN=2ccfc5d55b8c984e852458fb770bf78a65293af6; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=2368B76DB55E7B4F2296F3879CE79102:FG=1; BAIDU_WISE_UID=wapp_1637932884090_184; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=1; ZD_ENTRY=baidu; BDUSS=TZnbnFER2pVZm5aVXJUa2NhVDdzY0x-cE9lS0FCZDlPUUc5cDNDYXNmemFNc2xoRVFBQUFBJCQAAAAAAAAAAAEAAADdvB9azOzQqzU0MTg4YQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANqloWHapaFha; BDUSS_BFESS=TZnbnFER2pVZm5aVXJUa2NhVDdzY0x-cE9lS0FCZDlPUUc5cDNDYXNmemFNc2xoRVFBQUFBJCQAAAAAAAAAAAEAAADdvB9azOzQqzU0MTg4YQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANqloWHapaFha; H_PS_PSSID=34441_35104_31254_35049_34584_34517_34579_34606_35331_35317_26350_35209_35114_35301; BA_HECTOR=8ga50ha0252000ag4f1gq3gcl0q; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1637990807; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1637990807'
        }
        cookie_detect={
            "Cookie": "BIDUPSID=2368B76DB55E7B4FEE7A663ABACC0E4D; PSTM=1635161349; BAIDUID=2368B76DB55E7B4F2296F3879CE79102:FG=1; __yjs_duid=1_dc16c041a1fcac8aca74bdf2d71d8a4c1635172396343; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; HISTORY_SWITCH=1; USERTOKEN=2ccfc5d55b8c984e852458fb770bf78a65293af6; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=TZnbnFER2pVZm5aVXJUa2NhVDdzY0x-cE9lS0FCZDlPUUc5cDNDYXNmemFNc2xoRVFBQUFBJCQAAAAAAAAAAAEAAADdvB9azOzQqzU0MTg4YQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANqloWHapaFha; BDUSS_BFESS=TZnbnFER2pVZm5aVXJUa2NhVDdzY0x-cE9lS0FCZDlPUUc5cDNDYXNmemFNc2xoRVFBQUFBJCQAAAAAAAAAAAEAAADdvB9azOzQqzU0MTg4YQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANqloWHapaFha; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1637990807; BAIDUID_BFESS=2368B76DB55E7B4F2296F3879CE79102:FG=1; delPer=0; PSINO=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=34441_35104_31254_35049_34584_34517_34579_34606_35331_35317_26350_35209_35114_35301; BA_HECTOR=0485200ka105agak2i1gq3jc30r; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1637996764"
        }
        lang = self.parse_url(self.url_langdetect,lang_derect_data,cookie_detect)["lan"]
        sign = self.run_js()
        trans_data = {
            "from": "zh",
            "to": "en",
            "query": self.query,
            "transtype": "realtime",
            "simple_means_flag":"3",
            "sign":sign,
            "token": "77e13f5d36eae7193cf9587dd4643065",
            "domain":"common"
        } if lang == 'zh' else {
            "from": "en",
            "to": "zh",
            "query": self.query,
            "transtype": "realtime",
            "simple_means_flag":"3",
            "sign":sign,
            "token": "77e13f5d36eae7193cf9587dd4643065",
            "domain":"common"
        }
        result = self.parse_url(self.url_trans,trans_data,cookie_trans)['trans_result']['data'][0]['dst']
        print(result)
        return result
        
if __name__ == '__main__':
    query = sys.argv[1]
    translate = Translate(query)
    translate.run()
        