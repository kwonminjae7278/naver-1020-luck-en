# QA에서 찾은 문구·표시 고침 (chiring/index.html, 다시 실행해도 안전)
import os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = f'{D}/chiring/index.html'; s = open(P, encoding='utf-8').read()
FIX = [
    # 윤달 칩: 'Leap month'가 두 줄로 꺾이지 않게 글자 폭에 맞춤
    ('.chip--small{width:60px}', '.chip--small{width:auto;min-width:60px;padding:0 14px;white-space:nowrap}'),
    # 친구 카드: '친구에게 / 기운 보내기'
    ('children:[`Send energy`,(0,h.jsx)(`br`,{}),`Send Energy`]', 'children:[`Send energy`,(0,h.jsx)(`br`,{}),`to a friend`]'),
    # 리포트 칩: 태어난 시간 24시간 → 12시간 (AM/PM)
    ('u.birthTime??`Time unknown`]', '(u.birthTime?(([h,m])=>`${+h%12||12}:${m} ${+h<12?`AM`:`PM`}`)(u.birthTime.split(`:`)):`Time unknown`)]'),
]
for a, b in FIX:
    if a in s: s = s.replace(a, b); print('fixed:', b[:60])
    elif b in s: print('already:', b[:60])
    else: print('NOT FOUND:', a[:60])
open(P, 'w', encoding='utf-8').write(s)
