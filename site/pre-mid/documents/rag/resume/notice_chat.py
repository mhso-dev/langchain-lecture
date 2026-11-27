from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()  # 환경에 설정한 키를 읽습니다.
RULE = "소리채집 동아리 공지 도우미입니다. 사용자가 정정한 항목은 최신 내용을 사용하고 그대로 둔 항목은 유지하세요. 모임 정보가 없으면 어떤 정보가 필요한지 질문하세요."

def send(history, question):
    # 이번 입력에 user 역할을 붙이면 앞선 모델 답과 구별할 수 있습니다.
    user = {"role": "user", "content": question}
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=RULE,
        input=history + [user],  # 앞선 대화 뒤에 새 질문을 붙여 보냅니다.
        store=False,
    )
    reply = response.output_text
    # 응답을 받은 뒤에만 한 쌍을 기록하므로 실패한 질문은 이력에 남지 않습니다.
    history.extend([user, {"role": "assistant", "content": reply}])
    return reply
