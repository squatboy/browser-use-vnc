import asyncio
from dotenv import load_dotenv
from browser_use.llm import ChatGoogle, ChatOpenAI
from pydantic import BaseModel
from browser_use import Agent, BrowserSession
from browser_use.browser import BrowserSession

load_dotenv()

# ====================== 사용자 입력 정보 (테스트용 더미값) ======================
first_name = "JaeYoung"
last_name = "Lee"
email = "test@gmail.com"
country = "대한민국"
phone_number = "10-1234-5678"
gender = "남성"
birth_date_year = "2001"
birth_date_month = "3"
birth_date_day = "9"
passenger_passport_number = "M123456789"  # 여권 번호 예시
passenger_passport_expire_date = "2030-12-31"  # 여권 만료일 예시

# ====================== SENSITIVE_DATA ======================
SENSITIVE_DATA = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "country": country,
    "phone_number": phone_number,
    "gender": gender,
    "birth_date_year": birth_date_year,
    "birth_date_month": birth_date_month,
    "birth_date_day": birth_date_day,
    "passport_number": passenger_passport_number,
    "passport_expire_date": passenger_passport_expire_date,
}


# ====================== 사용자 프롬프트 정보 추출 ======================
class Flight(BaseModel):
    departure: str = "Seoul"
    arrival: str = "Tokyo"
    depart_date: str = "2025-08-20"
    return_date: str = "2025-08-25"
    num_people: str = "1"


flight = Flight()


# =========================== 날짜/항공 선택 ===========================
def flight_agent_task():
    return f"""
            ※ 절대 새로고침(페이지 강제 새로고침)은 하지 마세요.
            * 스크롤도 금지합니다.
        
            1. [출발편{flight.departure} 설정]
                - agoda.com에 접속합니다.
                - 상단 메뉴에서 "항공권"을 클릭합니다.
                - "왕복"을 선택합니다.
                - 다음 정보를 정확히 입력합니다.:
                - 출발지: {flight.departure}
                - 도착지: {flight.arrival}

                ✅ **가는날과 오는날 날짜 확인 및 설정 (필수 조건)**  
                    ✈️ 현재 설정된 날짜가 다음과 일치하는지 반드시 먼저 확인하세요:  
                    - 가는날: **{flight.depart_date}**  
                    - 오는날: **{flight.return_date}**

                    ⚠️ 위 날짜가 **이미 설정되어 있다면** 절대 수정하지 마세요.  
                    ⚠️ 위 날짜가 **설정되어 있지 않은 경우에만** 아래 순서에 따라 변경하세요:

                    🔹 **가는날({flight.depart_date})** 설정 방법:  
                        1) '가는날' 입력 필드를 클릭합니다.   
                        2) **{flight.depart_date}** 날짜를 찾아 **딱 한 번만 클릭**합니다.  
                        3) 날짜 필드에 **"{flight.depart_date}"**이 정확히 입력되었는지 시각적으로 확인합니다.

                    🔹 **오는날({flight.return_date})** 설정 방법:  
                        1) '가는날' 옆에 있는 '오는날'필드에 똑같이 {flight.depart_date}이 있으면 즉시 변경을 합니다.
                        1) **{flight.return_date}** 날짜를 찾아 **딱 한 번만 클릭**합니다.  
                        2) 날짜 필드에 **"{flight.return_date}"**이 정확히 표시되었는지 반드시 확인합니다.

                - 인원: 1명  
                - 좌석: 이코노미 클래스  

                - 위 항목들을 모두 정확히 입력한 후, **"검색" 버튼을 클릭**합니다.
            """


def go_travel():
    return """
    새로고침은 절대로 하지마.
    계열사 선택 금지.

    ✅ 1. 티웨이항공 필터 적용 (반복 금지)
        a. 좌측 필터 영역에서 '항공사' 섹션 찾기.
        b. '항공사 n곳 모두 보기' 클릭은 딱 한 번만.
        c. '티웨이항공' 체크박스 찾기 (안 보아면 스크롤 해서 찾기).
        d. 딱 한 번만 클릭해서 체크하기.
        e. 체크 상태로 바뀌면 다시 클릭 또는 해제 절대 금지.
        f. 필터 적용 확인 (목록 내 항공사명과 체크박스 상태).

    ✅ 2. 필터 적용 결과 확인
        a. 항공편 목록에 로딩 표시가 있으면 로딩이 끝날 때까지 대기합니다.
        b. 모든 항공편이 '티웨이항공' 인지 확인합니다.

    ✅ 3. 최저가 항공편 선택
        a. 필터링된 항공편 중 가장 저렴한 '티웨이항공' 항공편을 클릭합니다.
        b. 조건 만족되면 '선택하기' 버튼 클릭

    ---------------------------------------------------

    ※ 새로고침(페이지 강제 재로딩)은 절대 하지 말 것.  
    ※ 모든 이동은 페이지 내 UI 조작(클릭, 탭 전환 등)으로만 진행.  
    ※ 필터 적용 시 중복 클릭 금지, 필터 상태 유지 철저.
    
"""


def come_travel():
    return """
    새로고침은 절대로 하지마.
    계열사 선택 금지.
    ✅ 1. 오는편 페이지 전환 확인
        - 가는편 선택 후, 자동으로 오는편 페이지로 전환됩니다.
        - 별도 탭 전환이나 추가 클릭 없이 진행됩니다.

    ✅ 2. 티웨이항공 필터 적용 (반복 금지)
        a. 좌측 필터 영역에서 '항공사' 섹션 찾기.
        b. '항공사 n곳 모두 보기' 클릭은 딱 한 번만.
        c. '티웨이항공' 체크박스 찾기 (안 보아면 스크롤 해서 찾기).
        d. 딱 한 번만 클릭해서 체크하기.
        e. 체크 상태로 바뀌면 다시 클릭 또는 해제 절대 금지.
        f. 필터 적용 확인 (목록 내 항공사명과 체크박스 상태).

    ✅ 3. 필터 적용 결과 확인
        a. 항공편 목록에 로딩 표시가 있으면 로딩이 끝날 때까지 대기합니다.
        b. 모든 항공편이 '티웨이항공' 또는 '티웨이항공'인지 확인합니다.

    ✅ 4. 최저가 항공편 선택
        a. 필터링된 항공편 중 가장 저렴한 '티웨이항공' 항공편을 클릭합니다.
        b. 조건 만족되면 '선택하기' 버튼 클릭


    ---------------------------------------------------

    ※ 새로고침(페이지 강제 재로딩)은 절대 하지 말 것.  
    ※ 모든 이동은 페이지 내 UI 조작(클릭, 탭 전환 등)으로만 진행.  
    ※ 필터 적용 시 중복 클릭 금지, 필터 상태 유지 철저.

    """


# =========================== 예약자/탑승객 정보 입력 ===========================
def pay_agent_task():
    # SENSITIVE_DATA의 birth_date를 년, 월, 일
    birth_year = SENSITIVE_DATA["birth_date_year"]
    birth_month = SENSITIVE_DATA["birth_date_month"]
    birth_day = SENSITIVE_DATA["birth_date_day"]

    return f"""
            ## 예약 절차 진행 (정보 입력):

            1.  **연락처 정보 입력**: 연락처 정보 입력 섹션에 다음 정보를 입력하십시오.
                a. '영문 이름(First Name)' 필드에 `first_name`을 입력하십시오.
                b. '영문 성(Last Name)' 필드에 `last_name`을 입력하십시오.
                c. '이메일 주소' 필드에 `email`을 입력하십시오.
                d. '거주 국가/지역' 드롭다운 버튼을 클릭한 후, 드롭다운의 검색창에 `country`를 입력하고, 드롭다운 목록에 나타나는 `country`의 라디오 버튼 또는 옵션을 한 번 클릭하여 선택하십시오.
                e. '전화번호' 필드에 `phone_number`를 입력하십시오.

            2. **페이지 스크롤**: 연락처 정보 입력 후, 웹 페이지 하단으로 스크롤하여 다음 단계로 넘어가십시오.

            3. **탑승객 정보 (성인) 입력**: 이어서 탑승객 정보(성인) 섹션에 다음 정보를 입력하십시오.
                * **성별**: '성별' 항목에서 `gender` 값에 해당하는 성별 라디오 버튼을 한 번 클릭하여 선택하십시오. (예: `gender`가 "남성"이면 '남성' 라디오 버튼 클릭)
                * **영문 이름 및 영문 중간 이름**: '영문 이름 & 영문 중간 이름' 필드에 `first_name`을 입력하십시오. (중간 이름이 없다면 이름만 입력)
                * **영문 성**: '영문 성(Last Name)' 필드에 `last_name`을 입력하십시오.
                * **생년월일**: '생년월일' 섹션에 다음을 입력하십시오.
                    * '년도' 입력 필드에 {birth_year}을 입력하십시오.
                    * '월' 드롭다운 메뉴를 클릭하여 {birth_month}을 선택하십시오.
                    * '일' 입력 필드에 {birth_day}을 입력하십시오.
                * **국적**: '국적' 드롭다운 버튼을 클릭한 후, 검색창에 `country`를 입력하고, 드롭다운 목록에 나타나는 `country` 라디오 버튼 또는 옵션을 한 번 클릭하여 선택하십시오.
                    * **선택 후, 국적 필드에 `country`가 올바르게 표시되는지 확인하고, 재선택하지 마십시오.**
                * **여권 섹션**: (여권번호, 여권 발행 국적, 여권 만료일)
                    * **만약 여권 관련 정보 입력 항목 혹은 필드가 없다면 이 작업은 넘어가십시오!**
                    * '여권번호' 필드에 `passport_number`를 입력하십시오.
                    * '여권 발행 국가' 드롭다운 버튼을 클릭한 후, 검색창에 `country`를 입력하고, 드롭다운 목록에 나타나는 `country` 라디오 버튼 또는 옵션을 한 번 클릭하여 선택하십시오.
                        * **선택 후, 필드에 `country`가 올바르게 표시되는지 확인하고, 재선택하지 마십시오.**
                    * **여권 만료일**: '여권 만료일' 섹션에 다음을 입력하십시오.
                        * '년도' 입력 필드에 `passport_expire_date`의 연도 부분을 입력하십시오.
                        * '월' 드롭다운 버튼을 클릭하여 드롭다운 메뉴에서 `passport_expire_date`의 월 부분에 해당하는 라디오 버튼 또는 옵션을 한 번 클릭하여 선택하십시오.
                        * '일' 입력 필드에 `passport_expire_date`의 일 부분을 입력하십시오.

            4. **최종 동의 및 진행**:
                * "모든 항목에 동의합니다." 체크박스 클릭

            5. **부가서비스 및 여행 보험**:
                * 부가서비스와 여행 보험 등의 관련 항목은 사용하지 않거나 기본으로 선택되있는 옵션으로 결제 페이지로 이동하십시오.
            """


extend_planner_message = f"""
    REMEMBER the most important RULE:
    Make decisions at each stage carefully, and once done correctly, never repeat the task.
    If you find yourself setting the exact same 'Next goal' as the previous step, or performing the exact same action on the same element multiple times without the desired page change or a clear visual confirmation of success, critically re-evaluate:
    1. Is the goal truly not achieved, or am I misinterpreting the page state? (e.g., Did the filter *actually* apply even if I didn't see a spinner? Is the checkbox *already* checked?)
    2. Is the page still loading or updating from my previous action? Consider waiting a bit longer, especially if the task involves filtering or loading new content.
    3. Did I click the correct element? Is there a more specific or reliable element I should target (e.g., a checkbox directly associated with the text, or an element with a unique ID)? Double-check the element's properties.
    4. If an action is not working as expected after a couple of tries, do not repeat it endlessly. Re-assess the page, your understanding of the task, and consider a slightly different approach or element. For example, if clicking a checkbox isn't working, is there an "Apply" button I missed?
    Avoid getting stuck in a loop. If a specific action on a specific element isn't working, repeating it won't help. Assume your previous action *might* have worked and look for evidence.
    """


# =============== LLM ===============
llm = ChatGoogle(
    model="gemini-2.5-pro",
    temperature=0,
)

# =============== 브라우저 세션 ===============
browser_session = BrowserSession(
    keep_alive=True,  # 첫 번째 에이전트 완료 후에도 브라우저를 닫지 않음
    viewport={"width": 1200, "height": 1080},
    window_size={"width": 1200, "height": 1080},
    headless=False,
    args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
    ],
)

# =============== 1번째 에이전트 ===============
agent1 = Agent(
    task=flight_agent_task(),
    llm=llm,
    browser_session=browser_session,
    extend_system_message=extend_planner_message,
    sensitive_data=SENSITIVE_DATA,
)

# =============== 2번째 에이전트 ===============
agent2 = Agent(
    task=go_travel(),
    llm=llm,
    browser_session=browser_session,  # 같은 세션 재사용
    extend_system_message=extend_planner_message,
    sensitive_data=SENSITIVE_DATA,
)

# =============== 3번째 에이전트 ===============
agent3 = Agent(
    task=come_travel(),
    llm=llm,
    browser_session=browser_session,  # 같은 세션 재사용
    extend_system_message=extend_planner_message,
    sensitive_data=SENSITIVE_DATA,
)

# =============== 4번째 에이전트 ===============
agent4 = Agent(
    task=pay_agent_task(),
    llm=llm,
    browser_session=browser_session,  # 같은 세션 재사용
    extend_system_message=extend_planner_message,
    sensitive_data=SENSITIVE_DATA,
)


async def main():

    # ============= 브라우저 세션 시작 =============
    await browser_session.start()

    # =============== 1번째 에이전트 ===============
    await agent1.run(max_steps=100)

    # =============== 2번째 에이전트 ===============
    await agent2.run(max_steps=100)

    # =============== 3번째 에이전트 ===============
    await agent3.run(max_steps=100)

    # =============== 4번째 에이전트 ===============
    await agent4.run(max_steps=100)

    # ============= 브라우저 세션 종료 =============
    await browser_session.close()


if __name__ == "__main__":
    asyncio.run(main())
