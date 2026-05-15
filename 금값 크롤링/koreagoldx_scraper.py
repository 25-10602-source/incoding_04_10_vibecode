import urllib.request
import json
from datetime import datetime, timedelta
import csv

def scrape_gold_prices():
    # 1. 날짜 설정 (최근 1년)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    dataDateEnd = end_date.strftime("%Y.%m.%d")
    dataDateStart = start_date.strftime("%Y.%m.%d")
    
    # 2. API 엔드포인트 및 요청 데이터 구조
    url = "https://koreagoldx.co.kr/api/price/chart/list"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    payload = {
        "srchDt": "1Y",
        "type": "Au",
        "dataDateStart": dataDateStart,
        "dataDateEnd": dataDateEnd
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    print(f"데이터를 가져오는 중입니다... ({dataDateStart} ~ {dataDateEnd})")
    
    # 3. POST 요청 보내기
    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            price_list = response_data.get("list", [])
            
            if not price_list:
                print("성공적으로 요청했으나, 데이터가 없습니다.")
                return

            print(f"총 {len(price_list)}개의 시세 데이터를 찾았습니다.")
            
            # 4. CSV 파일로 저장
            csv_filename = "koreagoldx_prices_1year.csv"
            
            # API 응답의 key들을 가져와 CSV 헤더로 사용
            keys = price_list[0].keys()
            
            with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(price_list)
                
            print(f"성공적으로 데이터를 {csv_filename} 파일로 저장했습니다.")
            
            # 간단히 앞의 3개 데이터만 출력
            print("\n최근 3개 데이터 미리보기:")
            for i, item in enumerate(price_list[:3]):
                print(f"- {item['date']} | 내가 살 때(순금): {item.get('s_pure')} | 내가 팔 때(순금): {item.get('p_pure')}")
                
    except Exception as e:
        print(f"데이터를 가져오는데 실패했습니다: {e}")

if __name__ == "__main__":
    scrape_gold_prices()
