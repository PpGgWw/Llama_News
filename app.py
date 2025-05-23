from flask import Flask, render_template, request, redirect, url_for
from modules import naver_news_scraper # 새로운 모듈 임포트

# Flask 앱 초기화
app = Flask(__name__)

# 뉴스 스크래핑 함수 (예시 - 실제 구현 필요)
def scrape_naver_news(url):
    """지정된 URL에서 네이버 뉴스 본문을 스크래핑하는 함수"""
    print(f"Scraping content from: {url}")
    if "news.naver.com" in url:
        article_text = naver_news_scraper.extract_naver_news_content(url)
        return article_text
    else:
        return "유효하지 않은 네이버 뉴스 URL입니다."

# 신뢰도 판단 모델 함수 (예시 - 실제 구현 필요)
def analyze_trustworthiness(text):
    """텍스트를 입력받아 신뢰도 점수(%)를 반환하는 함수"""
    print("Analyzing trustworthiness...")
    # 여기에 머신러닝/딥러닝 모델 로직 구현
    # 예시 반환값:
    if text:
         # 텍스트 길이에 따라 임의의 점수 반환 (실제 모델 대체 필요)
        score = min(len(text) // 2, 95)
        return score
    else:
        return 0

# Llama 모델 분석 함수 (예시 - 실제 구현 필요)
def get_llama_analysis(text):
    """텍스트를 입력받아 Llama 모델의 분석 결과를 반환하는 함수"""
    print("Getting Llama analysis...")
    # 여기에 Llama 모델 API 호출 또는 로컬 모델 연동 로직 구현
    # 예시 반환값:
    if text:
        return """
        <p><strong>AI 분석 요약:</strong></p>
        <ul>
            <li>이 뉴스 기사는 특정 주장을 뒷받침하는 근거가 부족해 보입니다.</li>
            <li>일부 표현이 감정적이거나 편향된 시각을 나타낼 수 있습니다.</li>
            <li>관련된 다른 기사나 출처를 교차 확인하는 것이 좋습니다.</li>
        </ul>
        <p>(실제 Llama 모델 분석 결과는 더 상세하고 구체적일 것입니다.)</p>
        """
    else:
        return "<p>분석할 본문 내용이 없습니다.</p>"

# 메인 페이지 라우트
@app.route('/')
def index():
    """메인 입력 페이지를 렌더링합니다."""
    return render_template('index.html')

# URL 처리 및 결과 페이지 라우트
@app.route('/process', methods=['POST'])
def process_url():
    """입력받은 URL을 처리하고 결과 페이지를 렌더링합니다."""
    if request.method == 'POST':
        news_url = request.form.get('news_url') # form에서 'news_url' 이름으로 전송된 값 받기

        if not news_url:
            # URL이 없는 경우 다시 메인 페이지로 (간단한 오류 처리)
            return redirect(url_for('index'))

        # 1. URL에서 본문 스크랩
        article_content = scrape_naver_news(news_url)

        # 2. 신뢰도 점수 분석
        score = analyze_trustworthiness(article_content)

        # 3. Llama 모델 분석
        analysis = get_llama_analysis(article_content)

        # 4. 결과 페이지 렌더링 (결과 변수들 전달)
        return render_template('result.html',
                               score=score,
                               article_content=article_content,
                               analysis=analysis)
    else:
        # POST 요청이 아니면 메인 페이지로 리다이렉트
        return redirect(url_for('index'))

# 앱 실행 (같은 네트워크에서 접속 가능하도록 설정)
if __name__ == '__main__':
    # host='0.0.0.0' 추가: 모든 네트워크 인터페이스에서 접속 허용
    # debug=True는 개발 중에만 사용하세요.
    print(" * 로컬 네트워크에서 접속하려면 다음 주소를 사용하세요:")
    print(" * http://<본인 PC의 IP 주소>:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)