# 대화 기능 코드
# 구현 못 함
def handle_chat(user_message):
    # 사용자 메시지를 기반으로 챗봇 응답 생성
    if "happy" in user_message:
        return "That's great to hear! Let's find some upbeat music for you."
    elif "sad" in user_message:
        return "I'm here to cheer you up. Here's some soothing music."
    else:
        return "Tell me more about your day!"
