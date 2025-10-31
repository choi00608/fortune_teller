import google.generativeai as genai
from google import genai
import re

def extract_json_from_string(text: str) -> str | None:
    """
    문자열에서 JSON 마크다운(```json ... ```) 또는 
    일반적인 JSON ({...} 또는 [...]) 블록을 추출합니다.
    """
    # 1. ```json ... ``` 블록 찾기 (가장 안정적)
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    
    # 2. ``` ... ``` 블록 찾기
    match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)

    # 3. 문자열에서 가장 처음 나오는 '{'와 가장 마지막 '}'를 찾아 추출
    start_index = text.find('{')
    end_index = text.rfind('}')
    
    if start_index != -1 and end_index != -1 and end_index > start_index:
        return text[start_index:end_index+1]
        
    return None # JSON을 찾지 못함

def generate_saju_prompt(birth_info: dict) -> str:
    """입력 정보를 바탕으로 Gemini에게 보낼 프롬프트를 생성합니다."""
    
    prompt = f"""
당신은 사주(四柱)와 명리학(命理學)의 대가입니다. 
주어진 생년월일시와 태어난 지역 정보를 바탕으로, 웹 검색(Tool Use)을 활용하여 필요한 정보를 보충하고, 사주 팔자를 분석해주세요.
분석 결과는 아래에 명시된 JSON 형식에 맞춰서 상세하고 이해하기 쉽게 설명해야 합니다. 
각 항목에 대한 분석은 최소 50자 이상으로 구체적으로 작성해야 합니다.

# 입력 정보:
- 생년: {birth_info['year']}년
- 생월: {birth_info['month']}월
- 생일: {birth_info['day']}일
- 생시: {birth_info['hour']}시
- 태어난 지역: {birth_info['location']}
- 유저 질문: {birth_info['question']}

출력 양식:
  {{
  "saju_summary": "사주 전체에 대한 종합적인 요약 및 핵심 특징.",
  "year_pillar": {{
    "name": "연주(年柱)",
    "heavenly_stem": "연도의 천간 (예: 甲)",
    "earthly_branch": "연도의 지지 (예: 子)",
    "analysis": "연주가 상징하는 조상, 국가, 초년운(유년기)에 대한 상세한 분석."
  }},
  "month_pillar": {{
    "name": "월주(月柱)",
    "heavenly_stem": "월의 천간",
    "earthly_branch": "월의 지지",
    "analysis": "월주가 상징하는 부모, 형제, 사회, 청년운에 대한 상세한 분석."
  }},
  "day_pillar": {{
    "name": "일주(日柱)",
    "heavenly_stem": "일의 천간 (사주의 주체, '나' 자신)",
    "earthly_branch": "일의 지지 (나의 배우자, 개인적인 공간)",
    "analysis": "일주가 상징하는 '나' 자신의 성향, 배우자 운, 중년운에 대한 상세한 분석."
  }},
  "hour_pillar": {{
    "name": "시주(時柱)",
    "heavenly_stem": "시간의 천간",
    "earthly_branch": "시간의 지지",
    "analysis": "시주가 상징하는 자식, 직업, 말년운에 대한 상세한 분석."
  }},
  "five_elements": {{
    "analysis": "사주에 분포된 오행(목, 화, 토, 금, 수)의 균형과 상호작용에 대한 분석. 어떤 오행이 강하고 약한지, 그리고 그로 인해 나타나는 성향과 보완점에 대한 설명."
  }},
  "overall_luck": {{
    "early_life": "초년운(약 0~20세)에 대한 종합적인 설명.",
    "middle_age": "중년운(약 21~60세)에 대한 종합적인 설명.",
    "later_life": "말년운(약 61세 이후)에 대한 종합적인 설명."
  }},
  "today_luck": {{
    "love": "오늘의 사랑 운세에 대한 설명.",
    "career": "오늘의 직업 운세에 대한 설명.",
    "health": "오늘의 건강 운세에 대한 설명.",
    "wealth": "오늘의 재물 운세에 대한 설명."
  }},
  "answer":{{
    "analysis": "유저 질문에 대한 세부 운세 설명"
  }}
  }}
make sure to follow the JSON format exactly as shown above.
output the result in JSON format only.
no additional explanations outside the JSON format.
"""
    return prompt

def get_saju_analysis_from_gemini(prompt: str) -> dict | None:
    """Gemini API를 호출하여 사주 분석 결과를 가져옵니다."""
    try:
        client = genai.Client()
        
        print("\n⏳ Gemini가 사주를 분석하고 있습니다. 잠시만 기다려주세요...")
        
        response = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=prompt,
          config={
            "tools": [{"google_search": {}}],
          }
        )
        
        return response.text

    except Exception as e:
        print(f"\n[오류] API 호출 중 오류가 발생했습니다: {e}")
        return None
