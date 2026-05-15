import pandas as pd
import matplotlib.pyplot as plt

# Windows 기본 한글 폰트 설정 (맑은 고딕)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

def create_visualizations():
    print("데이터를 불러오는 중입니다...")
    df = pd.read_csv('koreagoldx_prices_1year.csv')

    # date 컬럼을 datetime으로 변환하고, 시간순으로 정렬
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    # 1. 순금(24K) 시세 추이 그래프
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['s_pure'], label='내가 살 때 (순금)', color='#D32F2F', linewidth=2)
    plt.plot(df.index, df['p_pure'], label='내가 팔 때 (순금)', color='#1976D2', linewidth=2)
    plt.title('최근 1년 순금(24K) 시세 추이', fontsize=16, pad=20)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('가격 (원)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('pure_gold_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" - 'pure_gold_trend.png' 이미지 저장 완료")

    # 2. 18K / 14K 시세 추이 그래프
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['s_18k'], label='내가 살 때 (18K)', color='#C2185B', linestyle='-', linewidth=1.5)
    plt.plot(df.index, df['p_18k'], label='내가 팔 때 (18K)', color='#0288D1', linestyle='-', linewidth=1.5)
    plt.plot(df.index, df['s_14k'], label='내가 살 때 (14K)', color='#F48FB1', linestyle='--', linewidth=1.5)
    plt.plot(df.index, df['p_14k'], label='내가 팔 때 (14K)', color='#81D4FA', linestyle='--', linewidth=1.5)
    plt.title('최근 1년 18K/14K 시세 추이', fontsize=16, pad=20)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('가격 (원)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('18k_14k_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" - '18k_14k_trend.png' 이미지 저장 완료")

    # 3. 은 / 백금 시세 추이 그래프
    # 백금과 은의 가격 단위가 크게 다를 수 있으므로 두 개의 y축 사용
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color_pt_s = '#7B1FA2'
    color_pt_p = '#BA68C8'
    ax1.set_xlabel('날짜', fontsize=12)
    ax1.set_ylabel('백금 가격 (원)', color=color_pt_s, fontsize=12)
    line1 = ax1.plot(df.index, df['s_white'], label='내가 살 때 (백금)', color=color_pt_s, linewidth=2)
    line2 = ax1.plot(df.index, df['p_white'], label='내가 팔 때 (백금)', color=color_pt_p, linewidth=2, linestyle='--')
    ax1.tick_params(axis='y', labelcolor=color_pt_s)
    
    ax2 = ax1.twinx()
    color_ag_s = '#616161'
    color_ag_p = '#BDBDBD'
    ax2.set_ylabel('은 가격 (원)', color=color_ag_s, fontsize=12)
    line3 = ax2.plot(df.index, df['s_silver'], label='내가 살 때 (은)', color=color_ag_s, linewidth=2)
    line4 = ax2.plot(df.index, df['p_silver'], label='내가 팔 때 (은)', color=color_ag_p, linewidth=2, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color_ag_s)

    lines = line1 + line2 + line3 + line4
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=11)

    plt.title('최근 1년 은 및 백금 시세 추이 (이중 Y축 적용)', fontsize=16, pad=20)
    ax1.grid(True, linestyle='--', alpha=0.6)
    fig.tight_layout()
    plt.savefig('silver_white_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" - 'silver_white_trend.png' 이미지 저장 완료")

    print("\n모든 시각화 작업이 이미지로 완료되었습니다!")

if __name__ == "__main__":
    create_visualizations()
