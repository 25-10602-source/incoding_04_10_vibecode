import requests
from datetime import datetime, timedelta
import re

def get_meal_info(date_str=None):
    """서울 자운고등학교 급식 정보를 나이스 open API를 통해 가져옵니다."""
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
        
    params = {
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": "B10", # 서울특별시교육청
        "SD_SCHUL_CODE": "7010703",  # 자운고등학교
        "MLSV_YMD": date_str         # 급식 일자 (YYYYMMDD)
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"=== {date_str[:4]}년 {date_str[4:6]}월 {date_str[6:]}일 자운고등학교 급식 ===")

        if "mealServiceDietInfo" in data:
            meal_data = data["mealServiceDietInfo"][1]["row"]
            
            for meal in meal_data:
                meal_type = meal.get("MMEAL_SC_NM", "급식")
                dishes = meal.get("DDISH_NM", "")
                calories = meal.get("CAL_INFO", "")
                
                # <br/> 태그를 줄바꿈으로 변경
                dishes_clean = dishes.replace("<br/>", "\n")
                
                # 원한다면 알레르기 번호 제거 주석 해제 (예: (1.2.3.) 형태 제거)
                # dishes_clean = re.sub(r'\([\d\.]+\)', '', dishes_clean)
                # 단독 숫자 및 점 제거 (예: 1.2.3. 제거)
                dishes_clean = re.sub(r'[\d\.]+', '', dishes_clean).strip()
                # 불필요한 빈 줄 제거
                dishes_clean = '\n'.join([line.strip() for line in dishes_clean.split('\n') if line.strip()])
                
                print(f"[{meal_type}] ({calories})")
                print(dishes_clean)
                print("--------------------------------------------------")
                
        elif "RESULT" in data and data["RESULT"]["CODE"] == "INFO-200":
            print("해당 날짜의 급식 정보가 없습니다. (급식이 없는 날일 수 있습니다)")
        else:
            print("급식 정보를 불러오는데 문제가 발생했습니다:", data)

    except Exception as e:
        print(f"진행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    print("메뉴를 선택해주세요.")
    print("1: 오늘 급식")
    print("2: 내일 급식")
    print("3: 특정 날짜 급식")
    
    choice = input("입력 (1/2/3): ").strip()
    
    if choice == "1":
        today = datetime.now().strftime("%Y%m%d")
        get_meal_info(today)
    elif choice == "2":
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
        get_meal_info(tomorrow)
    elif choice == "3":
        target_date = input("날짜를 입력하세요 (예: 20240510): ").strip()
        if len(target_date) == 8 and target_date.isdigit():
            get_meal_info(target_date)
        else:
            print("잘못된 날짜 형식입니다. YYYYMMDD 형태로 입력해주세요.")
    else:
        print("잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")
