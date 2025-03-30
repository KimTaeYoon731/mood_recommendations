// 엔터 키 처리 함수 추가
function handleKeyPress(event) {
    if (event.key === "Enter") {
        getRecommendations();
    }
}

async function getRecommendations() {
    const moodInput = document.getElementById('moodInput');
    const recommendationsDiv = document.getElementById('recommendations');
    const resetBtn = document.getElementById('resetBtn');
    
    if (!moodInput.value) {
        alert('기분을 입력해주세요!');
        return;
    }

    try {
        recommendationsDiv.innerHTML = '✨ 추천 목록을 가져오는 중... ✨';
        recommendationsDiv.classList.add('active');
        
        const response = await fetch('/get_recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mood: moodInput.value })
        });

        const data = await response.json();
        
        if (data.error) {
            recommendationsDiv.innerHTML = `😢 오류: ${data.error}`;
            return;
        }
        
        recommendationsDiv.innerHTML = data.recommendations;
        resetBtn.style.display = 'inline-block';
    } catch (error) {
        console.error('Error:', error);
        recommendationsDiv.innerHTML = `😢 오류가 발생했습니다: ${error.message}`;
    }
}

// 다시 추천받기 함수 수정
function resetRecommendations() {
    const moodInput = document.getElementById('moodInput');
    const currentMood = moodInput.value; // 현재 기분 저장
    getRecommendations(); // 같은 기분으로 새로운 추천 받기
}