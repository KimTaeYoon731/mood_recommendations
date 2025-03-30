from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)

# OpenAI API 키 설정
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API 키가 설정되지 않았습니다.")
    
openai.api_key = api_key

def get_recommendations(mood):
    try:
        print(f"받은 감정: {mood}")  # 디버깅용
        print(f"API 키: {api_key[:5]}...")  # API 키 앞부분만 출력
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 감정에 따라 영화와 음악을 추천해주는 전문가입니다. 각 추천에 대한 이유도 함께 설명해주세요."},
                {"role": "user", "content": f"지금 기분이 {mood}일 때 어울리는 영화 3개와 노래 3개를 추천해주세요. 각각의 추천 이유도 설명해주세요."}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {str(e)}")  # 디버깅용
        raise e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def recommend():
    try:
        mood = request.json.get('mood')
        if not mood:
            return jsonify({'error': '감정이 입력되지 않았습니다.'}), 400
        
        recommendations = get_recommendations(mood)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        print(f"서버 오류: {str(e)}")  # 디버깅용
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
