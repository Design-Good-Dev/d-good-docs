import os
from datetime import datetime

def generate_minutes(clova_text_path, agenda, attendees):
    """
    클로바 노트 텍스트 파일을 읽어 프로젝트 회의록 템플릿으로 변환합니다.
    """
    if not os.path.exists(clova_text_path):
        print(f"❌ Error: {clova_text_path} 파일을 찾을 수 없습니다.")
        return

    today_str = datetime.now().strftime("%y%m%d")
    full_date = datetime.now().strftime("%Y-%m-%d")
    
    # 요일 구하기
    days = ['월', '화', '수', '목', '금', '토', '일']
    weekday = days[datetime.now().weekday()]

    # 클로바 노트 파일 읽기
    try:
        with open(clova_text_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
        return

    # 템플릿 구성
    template = f"""# 📝 {today_str}_회의록

**일시**: {full_date} ({weekday}) {datetime.now().strftime("%H:%M")}
**참석자**: {attendees}
**안건**: {agenda}

---

## 💬 논의 내용 (by D-gle)

{content}

---

## ✅ 결정된 사항
- 

## 🚀 향후 할 일 (To-Do)
- [ ] 

## 🌈 Retrospective
> 💡 개인 회고는 [Retrospectives/](../Retrospectives/) 폴더에서 별도로 작성해 주세요.

## 🗓️ 다음 회의 일정
- 
"""
    # 저장 폴더 확인 (Meeting_Minutes는 상위 폴더에 위치)
    save_dir = os.path.join(os.path.dirname(__file__), "..", "Meeting_Minutes")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 저장 경로 설정
    filename = f"{today_str}_generated_minutes.md"
    save_path = os.path.join(save_dir, filename)
    
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"✅ 회의록 생성 완료: {save_path}")
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")

if __name__ == "__main__":
    # 사용자가 쉽게 수정할 수 있도록 입력을 받거나 기본값을 설정합니다.
    print("--- 📝 회의록 생성기 ---")
    file_path = input("클로바 노트 텍스트 파일명 (예: recording.txt): ") or "recording.txt"
    meeting_agenda = input("회의 안건: ") or "안건 미정"
    meeting_attendees = input("참석자: ") or "안주희, "

    generate_minutes(file_path, meeting_agenda, meeting_attendees)
