import requests
import json
import pandas as pd
from datetime import date, timedelta


class Fin_Api():

    def __init__(self, n):

        self.n = n
        self.today = date.today().strftime('%y-%m-%d')
        self.before = (date.today() - timedelta(6)).strftime('%y-%m-%d')
        self.links = {"적금": "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?&pageNo=", "예금": "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?&pageNo="}
        self.bank_code = {"020000": "은행", "030300": "저축은행"}

        self.df_final = self.upload()
        self.print_out()

    def upload(self):
        name = []
        prod = []
        code1 = []
        code2 = []
        join_deny = []
        max = []
        int1 = []
        int2 = []
        type = []
        save_trm = []
        bank_code = []
        prod_type = []

        for product, link in self.links.items():
            for code in self.bank_code.keys():
                params = {'auth': '48718782b895ffd23e389281a58c03a4', 'topFinGrpNo': str(code)}
                r = requests.get(link+str(1), params=params)
                data = r.json()

                for j in range(int(data['result']['max_page_no'])):
                    r = requests.get(link+str(j+1), params=params)
                    data = r.json()
                    raw1 = data['result']['baseList']
                    raw2 = data['result']['optionList']

                    for i in range(len(raw1)):
                        name.append(raw1[i]['kor_co_nm'])
                        prod.append(str(raw1[i]['fin_prdt_nm']).replace('\n', ' '))
                        code1.append(raw1[i]['fin_co_no']+raw1[i]['fin_prdt_cd'])
                        join_deny.append(raw1[i]['join_deny'])
                        max.append(raw1[i]['max_limit'])

                    for i in range(len(raw2)):
                        code2.append(raw2[i]['fin_co_no']+raw2[i]['fin_prdt_cd'])
                        int1.append(raw2[i]['intr_rate'])
                        int2.append(raw2[i]['intr_rate2'])
                        try:
                            type.append(raw2[i]['rsrv_type_nm'])
                        except:
                            type.append('-')
                        save_trm.append(raw2[i]['save_trm'])
                        bank_code.append(code)
                        prod_type.append(product)

        print("raw data update complete!")
        basic_info = pd.DataFrame({'bank_name': name, 'prod_name': prod, 'deny': join_deny, 'max': max}, index = code1)
        int_info = pd.DataFrame({'type': type, 'basic_int': int1, 'add_int': int2, 'save_trm': save_trm, 'bank_code': bank_code,'prod_type': prod_type}, index=code2)

        df_final = pd.merge(int_info, basic_info, how='left', left_index = True, right_index=True)
        df_final = df_final[df_final['deny'] == '1']
        df_final = df_final[~df_final['prod_name'].str.contains('장병')]
        df_final = df_final[~df_final['prod_name'].str.contains('장학')]

        df_final.to_csv(f'dataset/data_{self.today}.csv', encoding='utf-8')
        return df_final

    def print_out(self):
        n = self.n
        df_final = self.df_final
        trm = [12,24,36]
        for type in self.links.keys():
            for code, name in self.bank_code.items():
                text = str(f"* {self.today} 기준 [{name}] 세전 이자율 TOP{n} {type}(단위: %)\n")
                for i in trm:
                    df = df_final[(df_final['bank_code'] == str(code)) & (df_final['prod_type'] == str(type))]
                    df = df[df['save_trm'] == str(i)]
                    df = df.drop_duplicates()
                    df = df.sort_values(by=['basic_int'], ascending=False)

                    text = text+str(f"- 만기: {i}개월 \n")
                    for j in range(n):
                        a = df.iloc[j]
                        text = text+str(f"은행명: {a['bank_name']}, 상품명: {a['prod_name']}, 세전금리: {a['basic_int']}, 우대금리: {a['add_int']} \n")
                print(text)


if __name__ == '__main__':
    Fin_Api(n=3)

    a = 1
    b = 1
