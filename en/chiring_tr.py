# 영문판: 팀원 앱(chiring/index.html, 주파수·친구방·온보딩 리포트) 한국어 → 영어
# 1) CODE: 어순이 바뀌는 JSX·템플릿은 코드 조각째 교체   2) PIECES/PREFIX: 문자열 조각 단위 교체
# 사용: python3 en/chiring_tr.py   (원본 chiring/index.html을 직접 고침, 다시 실행해도 안전)
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from js_strings import scan
d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_ = f'{d}/chiring/index.html'
s = open(P_, encoding='utf-8').read()

CODE = [
    # 문서
    ('<html lang="ko">', '<html lang="en">'),
    ('<title>치링 주파수</title>', '<title>Chiring Frequency</title>'),
    # 오행 이름 (리포트·라벨 전체가 이 이름을 씀) + 한자 표기
    ('P={wood:{ko:`나무`', 'P={wood:{ko:`Wood`'), ('fire:{ko:`불`,hanja:`火`', 'fire:{ko:`Fire`,hanja:`火`'),
    ('earth:{ko:`흙`,hanja:`土`', 'earth:{ko:`Earth`,hanja:`土`'), ('metal:{ko:`금`,hanja:`金`', 'metal:{ko:`Metal`,hanja:`金`'),
    ('water:{ko:`물`,hanja:`水`', 'water:{ko:`Water`,hanja:`水`'),
    ('hn=e=>`${P[e].ko}(${P[e].hanja})`', 'hn=e=>`${P[e].ko} (${P[e].hanja})`'),
    # 조사(을/를) → 영어에는 없음
    ("jt=e=>/[aeiouy]$/i.test(e)?`를`:`을`", 'jt=e=>``'),
    # 지금 [나/Sumin]에게 / 필요한 기운은  →  What [you need / Sumin needs] / right now is
    ('children:[`지금 `,d?`나`:(0,h.jsx)(`em`,{style:{color:e.color},children:p.name}),`에게`,(0,h.jsx)(`br`,{}),`필요한 기운은`]',
     'children:[`What `,d?`you need`:(0,h.jsx)(h.Fragment,{children:[(0,h.jsx)(`em`,{style:{color:e.color},children:p.name}),` needs`]}),(0,h.jsx)(`br`,{}),`right now is`]'),
    # 지금 나에게는 / 어떤 기운이 필요할까?  ·  Sumin한테 / 어떤 기운을 보내줄까?
    ('children:[`지금 나에게는`,(0,h.jsx)(`br`,{}),`어떤 기운이 필요할까?`]', 'children:[`What energy`,(0,h.jsx)(`br`,{}),`do I need right now?`]'),
    ('children:[(0,h.jsx)(`em`,{className:`freq__name`,children:p.name}),`한테`,(0,h.jsx)(`br`,{}),`어떤 기운을 보내줄까?`]',
     'children:[`What energy should`,(0,h.jsx)(`br`,{}),`we send `,(0,h.jsx)(`em`,{className:`freq__name`,children:p.name}),`?`]'),
    # [나를/Sumin을] 위한 / 기운 생성중···  →  Creating energy / for [you/Sumin]···
    ('children:[d?`나를`:`${p.name}${jt(p.name)}`,` 위한`,(0,h.jsx)(`br`,{}),`기운 생성중`,',
     'children:[`Creating energy`,(0,h.jsx)(`br`,{}),d?`for you`:`for ${p.name}`,'),
    # [나에게 / Sumin님께] / 기운 [충전/선물] 완료!  →  Energy [recharged! / sent / to Sumin!]
    ('children:[d?`나에게`:(0,h.jsxs)(h.Fragment,{children:[(0,h.jsx)(`em`,{style:{color:He(me,m).color},children:p.name}),`님께`]}),(0,h.jsx)(`br`,{}),d?`기운 충전 완료!`:`기운 선물 완료!`]',
     'children:d?[`Energy`,(0,h.jsx)(`br`,{}),`recharged!`]:[`Energy sent`,(0,h.jsx)(`br`,{}),`to `,(0,h.jsx)(`em`,{style:{color:He(me,m).color},children:p.name}),`!`]'),
    # Jiwon님께서 / 선물한 기운  →  Energy gifted / by Jiwon
    ('children:[a.from,`님께서`,(0,h.jsx)(`br`,{}),`선물한 기운`]', 'children:[`Energy gifted`,(0,h.jsx)(`br`,{}),`by `,a.from]'),
    # 리포트: [불]의 기운을 가진 타입 → You’re a Fire Type
    ('children:[P[l.core].ko,`의 기운을 가진 타입`]', 'children:[`You’re a `,P[l.core].ko,` Type`]'),
    # 리포트: 생년월일 표기 2003-10-31 → Oct 31, 2003 · 음력(윤) → Lunar (leap)
    ('er=e=>e.replace(/-/g,`.`)', 'er=e=>{let[t,n,r]=e.split(`-`);return`${[`Jan`,`Feb`,`Mar`,`Apr`,`May`,`Jun`,`Jul`,`Aug`,`Sep`,`Oct`,`Nov`,`Dec`][+n-1]} ${+r}, ${t}`}'),
    ('`${u.calendar===`lunar`?`음력${u.leap?`(윤)`:``} `:``}${er(u.birthDate)}`', '`${u.calendar===`lunar`?`Lunar${u.leap?` (leap)`:``} `:``}${er(u.birthDate)}`'),
    # 태어난 시간 표기: 오후 11:52 → 11:52 PM
    ('Dn=e=>{let t=Tn(e);return`${t.ampm===`am`?`오전`:`오후`} ${t.hour}:${String(t.minute).padStart(2,`0`)}`}',
     'Dn=e=>{let t=Tn(e);return`${t.hour}:${String(t.minute).padStart(2,`0`)} ${t.ampm===`am`?`AM`:`PM`}`}'),
    # 변수가 들어간 문장
    ('`${n+1}번째 카드`', '`Card ${n+1}`'),
    ('`${p.name}에게 한마디 남겨줘`', '`Leave a note for ${p.name}`'),
    ('`${Ie[me].label} 참`', '`${Ie[me].label} charm`'),
    ('`${p.name}님이 잘되길 비는 중`', '`Wishing ${p.name} all the best`'),
    ('`이름 ${u} 고치기`', '`Edit name ${u}`'),
    ('`${b.slice(0,4)}년 음력 ${+b.slice(4,6)}월에는 윤달이 없어요`', '`There’s no leap month ${+b.slice(4,6)} in the lunar year ${b.slice(0,4)}`'),
    ('`${P[r].ko} 기운 최다`', '`Most ${P[r].ko}`'),
    ('`${P[c].ko} 기운 0`', '`Zero ${P[c].ko}`'),
    ('`${P[c].ko} 기운 부족`', '`Low ${P[c].ko}`'),
    ('`${P[r].ko} 기운이\\n가장 많아요`', '`${P[r].ko} energy\\nruns strongest`'),
    ('`${P[c].ko} 기운은\\n비어 있어요`', '`${P[c].ko} energy\\nis missing`'),
    ('`${P[c].ko} 기운이\\n조금 부족해요`', '`${P[c].ko} energy\\nruns a little low`'),
    ('`${P[t].ko}의중심`', '`${P[t].ko} at Heart`'),
    ('`${P[t].ko} 기운 쓰기`', '`Using ${P[t].ko}`'),
    ('`${P[i].ko} 기운 채우기`', '`Topping Up ${P[i].ko}`'),
    ('`${P[i].ko} 기운을\\n채워 보세요`', '`Top up your\\n${P[i].ko} energy`'),
    ('`${P[r].ko} 기운 과열 주의`', '`${P[r].ko} Overload`'),
    ('`${P[r].ko} 기운이 넘칠 땐\\n이것만 조심해요`', '`When ${P[r].ko} overflows,\\nwatch out for this`'),
    ('`찰떡 기운 ${P[i].ko}`', '`Best Match: ${P[i].ko}`'),
    ('`${P[i].ko} 기운 친구와\\n찰떡이에요`', '`You click with\\n${P[i].ko} friends`'),
    ('`내 사주에서 아쉬운 ${hn(i)} 기운이 강한 친구는 **나에게 없는 걸 자연스럽게 채워 주는** 사람이에요. 함께 있으면 마음이 편하고 일도 술술 풀려요.\\n${F[i].asFriend}\\n기운이 떨어진 날엔 이 친구에게 먼저 연락해 보세요. 치링에서 서로 기운을 주고받다 보면 둘 다 한층 단단해질 거예요.`',
     '`A friend with strong ${hn(i)} energy — the one your chart is missing — **naturally fills in what you don’t have.** Being around them feels easy, and things just flow.\\n${F[i].asFriend}\\nOn low-energy days, reach out to this friend first. Swap energy back and forth on Chiring, and you’ll both grow stronger.`'),
    ('`${P[i].ko} 기운을\\n채우면 풀려요`', '`Top up ${P[i].ko}\\nand things unlock`'),
    ('`내 사주엔 ${P[i].ko} 기운이 ${e.counts[i]===0?`하나도 없어서`:`적은 편이라`}, 행운 포인트를 전부 **${P[i].ko} 쪽**으로 맞췄어요.\\n행운 색은 **${l.colorName}**, 행운 숫자는 **${l.number.replace(` · `,`, `)}**, 행운 방향은 **${l.direction}**이에요. 하루 중에는 **${F[i].luckyWhen}**이 가장 잘 맞아요.\\n이걸 다 챙길 필요는 없어요. 옷이나 소품에 ${l.colorName} 하나를 더하거나, 중요한 일을 ${F[i].luckyWhen}에 잡는 것처럼 하나만 걸려도 충분해요. 작은 행운 포인트가 쌓이면 흐름이 조금씩 ${P[i].ko} 쪽으로 기울어요.`',
     '`Your chart ${e.counts[i]===0?`has no ${P[i].ko} energy at all`:`runs low on ${P[i].ko} energy`}, so every lucky point here leans **toward ${P[i].ko}.**\\nYour lucky color is **${l.colorName}**, your lucky numbers are **${l.number.replace(` · `,`, `)}**, and your lucky direction is **${l.direction}**. The best time of day for you is **${F[i].luckyWhen}**.\\nYou don’t need all of them. Add one ${l.colorName} piece to your outfit, or plan something important for ${F[i].luckyWhen} — one is enough. As small lucky points add up, your flow slowly tilts toward ${P[i].ko}.`'),
    ('`${F[i].luckyUse}\\n오늘 바로 해 볼 수 있는 행운 루틴은 ${F[i].routine}예요.\\n거창하게 바꾸지 않아도 괜찮아요. 일주일에 한두 번만 챙겨도 기운의 균형이 맞춰지면서, 막혀 있던 일이 **생각보다 수월하게 풀리는** 걸 느낄 수 있을 거예요.`',
     '`${F[i].luckyUse}\\nA lucky routine you can try today: ${F[i].routine}.\\nNo big changes needed. Even once or twice a week brings your energy back into balance, and stuck things start **moving more easily than you’d expect.**`'),
    # 주파수 내용 키워드: 영어로 적어도 맞는 기운을 고르도록 영어 단어를 함께 (한국어도 그대로 인식)
    ('{match:/전남친|전여친|재회|연락|헤어|이별|썸|짝사랑|연애/', '{match:/전남친|전여친|재회|연락|헤어|이별|썸|짝사랑|연애|\\bex\\b|breakup|broke up|text|crush|dating|love|relationship/i'),
    ('{match:/시험|공부|면접|발표|과제|자격증|합격|수능/', '{match:/시험|공부|면접|발표|과제|자격증|합격|수능|exam|test|study|interview|presentation|assignment|pass|finals/i'),
    ('{match:/잠|피곤|야근|지쳐|지친|번아웃|쉬고/', '{match:/잠|피곤|야근|지쳐|지친|번아웃|쉬고|sleep|tired|exhausted|overtime|burnout|burned out|rest/i'),
    ('{match:/우울|힘들|슬프|슬퍼|속상|눈물|외로/', '{match:/우울|힘들|슬프|슬퍼|속상|눈물|외로|sad|depressed|down|upset|cry|lonely|hard time|rough/i'),
    ('{match:/돈|월급|용돈|통장|지갑|알바|주식/', '{match:/돈|월급|용돈|통장|지갑|알바|주식|money|salary|paycheck|wallet|savings|stock|broke|spend/i'),
    ('{match:/아프|감기|병원|다쳤|건강/', '{match:/아프|감기|병원|다쳤|건강|sick|cold|hospital|hurt|health|ill/i'),
    ('{match:/화나|짜증|싸웠|열받|빡/', '{match:/화나|짜증|싸웠|열받|빡|angry|mad|annoyed|fight|fought|pissed/i'),
    ('Be={water:/진정|재회|연락|전남친|전여친|화나|짜증|열받|긴장|생각|화해|싸웠/', 'Be={water:/진정|재회|연락|전남친|전여친|화나|짜증|열받|긴장|생각|화해|싸웠|calm|\\bex\\b|text|angry|annoyed|nervous|overthink|make up|fight|Calm Down/'),
    ('fire:/자신감|열정|에너지|발표|면접|용기|도전/', 'fire:/자신감|열정|에너지|발표|면접|용기|도전|confiden|passion|energy|presentation|interview|courage|challenge|Confidence|Energy Boost/'),
    ('wood:/새 인연|기분 전환|성장|시작|설렘|위로|멘탈/', 'wood:/새 인연|기분 전환|성장|시작|설렘|위로|멘탈|new love|mood|grow|start|fresh|comfort|mental|New Love|Mood Up|Comfort|Reset/'),
    ('metal:/금전|돈|대박|합격|집중|절약|월급|시험/', 'metal:/금전|돈|대박|합격|집중|절약|월급|시험|money|jackpot|pass|focus|saving|salary|exam|Money Luck|Jackpot|Saving|Pass Luck|Focus/'),
    ('earth:/꿀잠|휴식|건강|안정|피곤|쉬|아프/', 'earth:/꿀잠|휴식|건강|안정|피곤|쉬|아프|sleep|rest|health|stable|tired|sick|Sleep Well|Rest|Get Well/'),
    ('let n=/전남친|전여친|재회|연락/.test(t)', 'let n=/전남친|전여친|재회|연락|\\bex\\b|breakup|text/i.test(t)'),
    # 친구 기운 선물 메시지 (카드 뒷면, ZEN SERIF 네 줄)
]

PIECES = {
    # 하단 내비 · 공통
    '홈': 'Home', '아카이브': 'Archive', '친구방': 'Friends', '기운 충전': 'Energy',
    '라이팅 아카이브 기능은 곧 열릴 예정이에요.': 'Your writing archive is coming soon.',
    ' 화면은 곧 만들 예정이에요': ' is coming soon',
    '닫기': 'Close', '뒤로': 'Back', '좋아요': 'Like', '설정': 'Settings', '확인': 'Got it',
    '이전': 'Back', '다음': 'Next', '선택': 'Select', '완료': 'Done',
    # 주파수 카드 이름 (카드 이미지 라벨)
    '미련 폭파 기운': 'Blast the Past', '연락 말고 그냥 자 주파수': 'Don’t Text, Just Sleep',
    '새로운 인연이 들어오는 기운': 'New Faces Incoming', '새출발 풀충전': 'Fresh Start, Fully Charged',
    '합격 싹 틔우는 기운': 'Sprouting a Pass', '적게 일하고 많이 받는 기운': 'Work Less, Earn More',
    '지갑닫는 주파수': 'Wallet-Closing Frequency', '가만히 있어도 살 10kg 빠지는 주파수': 'Burn It While You Chill',
    '10000 칼로리 태워주는 기운': '10,000-Calorie Burn', '일단 진정 기운': 'Calm Down First',
    '차곡차곡 쌓아올리기': 'Stack It Up', '마음을 식히는 주파수': 'Cool-Down Frequency',
    '스트레스 싹 씻어내는 기운': 'Wash the Stress Away',
    # 오행 라벨
    '물 (水)': 'Water (水)', '나무 (木)': 'Wood (木)', '금 (金)': 'Metal (金)', '불 (火)': 'Fire (火)', '흙 (土)': 'Earth (土)',
    # 키워드 칩
    '마음 진정': 'Calm Down', '새 인연 찾기': 'New Love', '기분 전환': 'Mood Up', '멘탈 회복': 'Reset', '꿀잠 자기': 'Sleep Well',
    '합격 기운': 'Pass Luck', '집중력': 'Focus', '긴장 완화': 'Ease Nerves', '자신감': 'Confidence', '에너지 충전': 'Energy Boost',
    '휴식': 'Rest', '위로': 'Comfort', '금전운': 'Money Luck', '대박 기운': 'Jackpot', '절약': 'Saving', '건강 회복': 'Get Well', '화해': 'Make Up',
    # 필요한 기운 확인 (부제 · 이름 · 태그)
    '활활 타오르는\n연락 충동을 잠재워 주는': 'Puts out that\nburning urge to text', '물부처의 기운': 'Water Buddha',
    '# 물의 기운': '# Water energy', '# 새로운 인연의 기운': '# New connections', '# 연락충동에 찬물을 얹는': '# Cold water on the urge to text',
    '뜨거워진 마음을\n차분하게 식혀 주는': 'Gently cools down\na heated heart', '# 마음 진정': '# Calm down', '# 생각을 비우는': '# Clear your mind',
    '움츠러든 마음에\n불씨를 지펴 주는': 'Lights a spark\nin a shrinking heart', '불부처의 기운': 'Fire Buddha', '# 불의 기운': '# Fire energy',
    '# 자신감 충전': '# Confidence boost', '# 용기 한 스푼': '# A spoonful of courage',
    '새로운 시작에\n싹을 틔워 주는': 'Sprouts new beginnings\nfor a fresh start', '나무부처의 기운': 'Wood Buddha', '# 나무의 기운': '# Wood energy',
    '# 새로운 시작': '# New beginnings', '# 기분 전환': '# Mood up',
    '흩어진 운을\n단단하게 모아 주는': 'Gathers scattered luck\nand holds it tight', '금부처의 기운': 'Metal Buddha', '# 금의 기운': '# Metal energy',
    '# 합격 기운': '# Pass luck', '# 행운 모으기': '# Collecting luck',
    '지친 몸과 마음을\n포근하게 감싸 주는': 'Wraps a tired body\nand mind in comfort', '흙부처의 기운': 'Earth Buddha', '# 흙의 기운': '# Earth energy',
    '# 꿀잠 자기': '# Sleep well', '# 푹 쉬기': '# Rest up',
    # 친구가 보낸 메시지 (카드 뒷면, 네 줄)
    '미련은 오늘로\n싹 다 폭파!\n넌 더 좋은 사람\n만날 거야': 'Blow up those\nregrets today!\nYou’ll meet\nsomeone better',
    '저번처럼 백퍼\n후회한다 진짜..\n연락하지 말고\n잠이나 자 ㅡㅡ': 'You’ll regret it\nlike last time..\ndon’t text him,\njust sleep -_-',
    '올해는 진짜\n좋은 사람 온다\n소개팅 들어오면\n무조건 나가!': 'This year, the\nright one’s coming\nif you get a setup,\njust go!',
    '오늘은 아무것도\n하지 말고\n칠 모드 ON\n푹 쉬어': 'Do nothing\ntoday —\nchill mode ON\nrest up',
    '화날 땐\n일단 숨 크게\n열 번만 쉬고\n얘기하자': 'When you’re mad,\ntake ten\ndeep breaths,\nthen we talk',
    '스트레스는\n오늘로 싹\n씻어내고\n개운하게 자!': 'Wash all\nthat stress\naway tonight\nand sleep tight!',
    '새로운 시작\n완전 응원해\n충전 100%로\n가보자고!': 'Rooting for\nyour fresh start\nat 100% charge,\nlet’s go!',
    '너는 원래\n잘하는 사람이야\n이제 활짝\n필 차례!': 'You’ve always\nbeen great at this\nnow it’s your\nturn to bloom!',
    '이번엔 진짜\n합격이다\n붙으면 밥\n쏘는 거 알지?': 'This time\nyou’re passing\nand dinner’s\non you, right?',
    '오늘은 적당히\n일하고\n월급은 두 배로\n받자': 'Work just\nenough today\nand get paid\ndouble',
    '장바구니\n그만 담아..\n이번 달은\n지갑 닫기!': 'Stop adding\nto your cart..\nthis month,\nwallet closed!',
    '세이빙 모드\nON\n통장 잔고\n꼭 지켜!': 'Saving mode\nON\nprotect that\nbalance!',
    '일단 나가서\n걷기라도 해\n움직이면\n기분도 풀려': 'Just get out\nand take a walk\nonce you move,\nyou’ll feel better',
    '오늘도\n충분히 잘했어\n가만히 있어도\n빛나는 너': 'You did\nmore than enough\ntoday — you shine\neven standing still',
    '운동 같이\n가자고 했지?\n내일 아침\n7시 헬스장!': 'You said we’d\nwork out, right?\ntomorrow,\n7am, the gym!',
    '일단 진정하고\n숨 크게 쉬어\n다 잘\n될 거야': 'Calm down first\nand breathe deep\nit’s all going\nto be okay',
    '하나씩\n쌓으면 돼\n너 지금\n잘하고 있어': 'Just stack it\none at a time\nyou’re doing\nso well',
    '차곡차곡\n모으다 보면\n어느새\n큰 산이 돼 있을걸': 'Keep stacking\nlittle by little\nand soon it’ll\nbe a mountain',
    # 주파수 다시 듣기 · 카드
    '기운 주파수 듣기': 'Listen to Frequency', '친구': 'Friend',
    '카드 앞면 보기': 'View card front', '메세지 보기': 'View message',
    '눌러서 카드 확인하기': 'Tap to see your card', '눌러서 메세지 확인하기': 'Tap to read the message', '재생하기': 'Play',
    # 재생 화면 상태 문구
    '연락 충동이 억제되는 중···': 'Holding back the urge to text···', '마음의 온도를 낮추는 중···': 'Cooling down your heart···',
    '생각을 비워내는 중···': 'Clearing your mind···', '차분한 물 기운이 스며드는 중···': 'Calm Water energy seeping in···',
    '몸에 열정이 차오르는 중···': 'Passion rising in your body···', '움직일 힘이 생기는 중···': 'Finding the energy to move···',
    '불의 기운이 타오르는 중···': 'Fire energy blazing up···', '지친 마음에 불을 붙이는 중···': 'Relighting a tired heart···',
    '새로운 시작을 준비하는 중···': 'Getting ready for a fresh start···', '합격의 싹이 자라는 중···': 'Growing the seeds of success···',
    '나무 기운이 뻗어 나가는 중···': 'Wood energy branching out···', '마음에 새싹이 돋는 중···': 'New sprouts in your heart···',
    '지갑이 단단해지는 중···': 'Tightening your wallet···', '흩어진 마음을 정리하는 중···': 'Gathering a scattered mind···',
    '금 기운이 모이는 중···': 'Metal energy coming together···', '통장 잔고를 지키는 중···': 'Guarding your bank balance···',
    '마음이 차분히 가라앉는 중···': 'Your mind is settling down···', '기초를 단단히 다지는 중···': 'Building a solid base···',
    '흙 기운이 쌓이는 중···': 'Earth energy piling up···', '하나씩 쌓아 올리는 중···': 'Stacking it up, one by one···',
    '주파수 기운 충전 완료!': 'Frequency energy fully charged!',
    '5초 뒤로': 'Back 5 seconds', '일시정지': 'Pause', '재생': 'Play', '5초 앞으로': 'Forward 5 seconds',
    # 친구 이름 (높임 표기 → 영문 이름)
    '다윤': 'Dayun', '수민': 'Sumin', '다현': 'Dahyun', '나현': 'Nahyun', '유진': 'Yujin', '민재': 'Minjae', '수진': 'Sujin',
    '나': 'Me',
    # 기운 선물 흐름
    '어떤 친구에게': 'Who should', '기운을 보내줄까?': 'get your energy?', '오늘 필요한 기운: ': 'Needs today: ',
    '요즘 나는 어떤 상태인지 적어주세요': 'Write how you’ve been feeling lately', '친구에게 필요한 상황을 적어주세요': 'Write what your friend is going through',
    '탭하여 요즘 내 상황을 적어주세요': 'Tap to write how you’re doing', '탭하여 내용을 입력해주세요': 'Tap to write what’s going on',
    '어떤 마음을 채우고 싶어?': 'What do you want to fill up on?', '어떤 마음을 전해주고 싶어?': 'What do you want to send?',
    '키워드 입력': 'Add a keyword', '직접 작성하기': 'Custom',
    '주파수 만들기': 'Create Frequency', '나의 주파수': 'My Frequency', '주파수 선물하기': 'Gift a Frequency',
    '나에게 해주고 싶은 말을 남겨줘': 'Leave a note for yourself', '기운 채우기': 'Recharge', '기운 보내기': 'Send Energy',
    '마음을 담아 카드를 문질러주세요': 'Rub the card with all your heart', '나에게 좋은 기운을 모으는 중': 'Gathering good energy for you',
    # 기운 충전 홈
    '오늘의 기운 충전': 'Today’s Recharge', '필요한 기운을 나를 위해 채우거나 친구에게 보내보세요.': 'Recharge the energy you need, or send it to a friend.',
    '나를 위한': 'Recharge', '내 기운 채우기': 'my energy', '친구에게': 'Send energy',
    '기운 주파수 다시 듣기': 'Replay Frequencies', '오늘 부족한 ': 'Low on ', '의 기운, 지난 주파수로 채워봐요.': '? Top up with past frequencies.',
    # 설정
    '시스템': 'System', '라이트': 'Light', '다크': 'Dark', '화면 모드': 'Appearance', '알림': 'Notifications',
    '오늘의 기운 알림': 'Daily energy alert', '매일 아침 오늘 필요한 기운을 알려 드려요': 'Every morning, we’ll tell you the energy you need',
    '사주 계산': 'Birth chart', '서울 시간 보정': 'Seoul time correction', '태어난 시간에서 30분을 빼서 계산해요': 'Calculates with 30 minutes subtracted from your birth time',
    '야자시 적용': 'Late-night hour rule', '밤 11~12시 출생은 일주를 그날로 봐요': 'Births from 11pm to midnight count as that same day',
    '내 정보': 'My info', '사주 정보 수정하기': 'Edit birth details', '한 번 더 누르면 모두 지워져요': 'Tap once more to erase everything',
    '입력한 정보 모두 지우기': 'Erase all my info', '치링 v': 'Chiring v', '사진을 열 수 없어요': 'Couldn’t open the photo',
    # 천간·지지 (화면에 표시용 한글 음 → 로마자)
    '갑': 'Gap', '을': 'Eul', '병': 'Byeong', '정': 'Jeong', '무': 'Mu', '기': 'Gi', '경': 'Gyeong', '신': 'Sin', '임': 'Im', '계': 'Gye',
    '자': 'Ja', '축': 'Chuk', '인': 'In', '묘': 'Myo', '진': 'Jin', '사': 'Sa', '오': 'O', '미': 'Mi', '유': 'Yu', '술': 'Sul', '해': 'Hae',
    '비견': 'Peer', '겁재': 'Rival', '식신': 'Talent', '상관': 'Rebel', '편재': 'Windfall', '정재': 'Steady Wealth',
    '편관': 'Pressure', '정관': 'Authority', '편인': 'Intuition', '정인': 'Support',
    # 사주 설정
    '오전': 'AM', '오후': 'PM', '사주 설정': 'Birth Details', '프로필 사진 고르기': 'Choose profile photo', '이름': 'Name',
    '생년월일': 'Date of Birth', '양력': 'Solar', '음력': 'Lunar', '윤달': 'Leap month', '생년월일 8자리': 'Date of birth, 8 digits',
    '날짜를 다시 확인해 주세요': 'Please check the date again', '태어난 시간': 'Time of Birth', '모르면 비워 둬도 괜찮아요': 'Leave blank if you’re not sure',
    '태어난 시간 지우기': 'Clear time of birth', '성별': 'Gender', '남자': 'Male', '여자': 'Female',
    '캐해 분석 중…': 'Reading your vibe…', '나의 캐해 확인하기': 'Reveal My Vibe', '오전 오후': 'AM / PM', '시': 'Hour', '분': 'Minute',
    # 리포트 공통
    '숨겨진 에너지': 'Hidden Energy', '마이웨이': 'My Way', '흡수력 만렙': 'Max-Level Absorber', '표현 장인': 'Expression Master', '현실 감각': 'Reality Sense',
    '나의 오행': 'My Elements', '핵심 성향': 'Core Traits', '내 기운 사용법': 'Energy Playbook', '주의 포인트': 'Watch-Outs',
    '충전 신호': 'Recharge Signals', '지칠 땐\n이런 신호가 와요': 'When you’re drained,\nthese signs show up', '관계 속 나': 'Me & My People',
    '친구들이 보는 나': 'How Friends See Me', '행운 포인트': 'Luck Boosters', '이렇게 써먹어요': 'How to use it',
    '여성': 'Female', '남성': 'Male', '시간 모름': 'Time unknown', '나의 캐해 리포트': 'My Vibe Report',
    # 오행별 짧은 항목
    '아침': 'morning', '민트 그린': 'Mint Green', '동쪽': 'East', '한낮': 'midday', '핫 핑크': 'Hot Pink', '남쪽': 'South',
    '늦은 오후': 'late afternoon', '선셋 오렌지': 'Sunset Orange', '중앙': 'Center', '해 질 녘': 'dusk', '네온 라임': 'Neon Lime', '서쪽': 'West',
    '밤': 'night', '아쿠아 블루': 'Aqua Blue', '북쪽': 'North',
    '**아침 일찍** 공원이나 숲길을 걷고, 책상 위 **작은 화분**에 물 주기': 'taking an **early morning** walk through a park or forest path, then watering the **little plant** on your desk',
    '**한낮**엔 햇살 드는 카페 창가 자리, 밤엔 **향초** 하나 켜 두기': 'grabbing a sunny café window seat at **midday**, and lighting a **scented candle** at night',
    '**늦은 오후**, 집 근처에서 **도자기 머그**에 따뜻한 차 한 잔 마시기': 'having a warm cup of tea from a **ceramic mug** near home in the **late afternoon**',
    '**해 질 무렵** 서점에 들르고, **실버 액세서리** 하나 챙기기': 'stopping by a bookstore **around dusk** and wearing one **silver accessory**',
    '**밤 산책**은 물가 쪽으로, 자기 전 **텀블러**에 물 가득 채워 두기': 'taking your **night walk** along the water, and filling your **tumbler** before bed',
    '시작하는 자리에서\n가장 빛나요': 'You shine brightest\nwhen starting things', '앞장서는\n든든한 기둥': 'The solid pillar\nwho leads the way',
    '보여 주고 말할 때\n가장 빛나요': 'You shine brightest\nwhen you show and speak', '분위기를 띄우는\n무드 메이커': 'The mood maker\nwho lifts the room',
    '꾸준히 쌓을 때\n가장 빛나요': 'You shine brightest\nwhen you build steadily', '언제 가도 있는\n편안한 쉼터': 'The cozy shelter\nthat’s always there',
    '정리하고 마무리할 때\n가장 빛나요': 'You shine brightest\nwhen you wrap things up', '할 말은 하는\n의리파': 'The loyal one\nwho says what’s needed',
    '깊이 파고들 때\n가장 빛나요': 'You shine brightest\nwhen you dig deep', '속 깊은\n공감 요정': 'The deep-hearted\nempathy fairy',
    # 일간 10가지 타입 제목
    '곧게 뻗어 가는\n타고난 리더': 'Growing straight up,\na born leader', '부드럽지만,\n어디서든 살아남아요': 'Soft, but you\nthrive anywhere',
    '있기만 해도\n분위기가 환해져요': 'Just by being there,\nyou light up the room', '조용하지만,\n한번 붙으면 오래 가요': 'Quiet at first,\nbut once you’re lit, you last',
    '흔들리지 않는\n든든한 산': 'A steady mountain\nthat never shakes', '모든 걸 품어 주는\n다정한 들판': 'A gentle field\nthat holds everything',
    '단단하고,\n결정은 시원하게': 'Solid, and\ndecisive', '날카롭게 빛나는\n감각의 보석': 'A sharp, shining\ngem of taste',
    '깊고 넓게,\n멀리 흘러가요': 'Deep and wide,\nyou flow far', '조용히 스며들어\n마음을 적셔요': 'Quietly seeping in,\nyou soften hearts',
    # 중심×주변 조합 제목 (25)
    '숲을 이룬 나무,\n함께일 때 더 단단해요': 'A tree in a forest,\nstronger together', '꽃을 피우려\n쉬지 않고 자라는 나무': 'A tree that never stops\ngrowing toward bloom',
    '넓은 땅에\n깊게 뿌리내린 나무': 'A tree rooted deep\nin wide-open land', '도끼질에도 꺾이지 않고\n다듬어지는 나무': 'A tree that doesn’t break\nunder the axe, but takes shape',
    '물을 머금고\n천천히 크게 자라는 나무': 'A tree that drinks deep\nand grows slow and tall',
    '모일수록\n더 크게 번지는 불꽃': 'A flame that spreads\nbigger the more it gathers', '주변을 따뜻하게\n데워 주는 화로': 'A hearth that keeps\neveryone around it warm',
    '단단한 쇠도 녹여\n모양을 만드는 불': 'A fire that melts\nhard steel into shape', '차가운 물 속에서도\n꺼지지 않는 불씨': 'A spark that stays lit,\neven in cold water',
    '장작을 품고\n오래 타오르는 불': 'A fire that holds its logs\nand burns long',
    '겹겹이 쌓여\n흔들리지 않는 산': 'A mountain built in layers\nthat never shakes', '속에 보석을\n품고 있는 땅': 'Land with gems\nhidden inside',
    '물길을 품어\n생명을 키우는 땅': 'Land that holds streams\nand grows life', '뿌리를 받아 내며\n더 단단해지는 땅': 'Land that holds roots\nand grows firmer',
    '햇볕에 데워진\n따뜻한 땅': 'Warm land\nheated by the sun',
    '부딪힐수록\n더 빛나는 금속': 'Metal that shines\nbrighter with every hit', '맑은 물을 길어 올리는\n샘가의 바위': 'A rock by the spring\ndrawing up clear water',
    '나무를 다듬어\n쓸모를 만드는 칼': 'A blade that shapes wood\ninto something useful', '뜨거운 불에\n단련되는 강철': 'Steel tempered\nin a hot fire',
    '흙 속에서 천천히\n빛을 키우는 원석': 'A raw gem slowly growing\nits shine in the earth',
    '모여서 큰 흐름이 되는\n물줄기': 'Streams that gather\ninto a great current', '숲을 키우며\n흘러가는 시냇물': 'A brook that flows on\nand feeds the forest',
    '햇살을 받아\n반짝이는 수면': 'A surface that sparkles\nin the sunlight', '둑을 만나\n깊어지는 호수': 'A lake that deepens\nwhen it meets a dam',
    '바위 틈에서\n끝없이 솟는 샘물': 'A spring that wells up\nendlessly from the rocks',
    '오늘 행운 담기_참': 'Save Today’s Luck — Charm',
}

PREFIX = {
    # 일간 10가지 타입 본문
    '큰 나무처럼 **위로 곧게': 'Like a tall tree, you have **the drive to grow straight up.** Once you set a goal, you head right for it without detours, and people naturally want to lean on your steadiness.\nYour pride runs deep, so **bending can feel hard sometimes**, but that straightness is exactly what earns people’s trust. You keep your word, and you hold your ground until the job is done.\nNow and then, let the wind sway your branches a little. Remember that **a tree that can bend grows even taller**, and you’ll reach much farther than you are now.',
    '꽃과 덩굴처럼 **유연하게': 'Like flowers and vines, you’re **the type who flexibly finds a way.** You adapt fast when things change, and you have a great sense for reading the room.\nYou may look delicate, but you’re tough inside, with the grit to **bloom in any crack you can find.** Instead of crashing head-on, you’re wise enough to find a way around, so you always end up with an answer, even when you’re stuck.\nBut while you adjust to others, you can lose sight of where you want to go. Keep **a good eye for what to lean on**, and you’ll bloom beautifully wherever you are.',
    '태양처럼 **밝고 솔직한': 'Like the sun, you carry **bright, honest energy.** You’re bad at hiding things, so your feelings show on your face, but that openness is exactly why people warm up to you so easily.\nYou’re great at starting things, with a real talent for **setting the stage and bringing people together.** You raise your hand first while others hesitate, and you can turn a heavy mood bright in an instant.\nBut just as the sun can’t blaze all day, you need your rest too. Remember that **recharging is a skill if you want to stay bright**, and your warmth will reach even farther.',
    '평소에는 차분하고 조용해 보여도, 마음을 정하면 **쉽게': 'You may seem calm and quiet most days, but once you decide, **you rarely give up.**\nYou don’t make a show of it, yet there’s real drive and a strong sense of your own standards underneath. Like a candle, you have the warmth to **light up the people close to you for a long time**, and a rare ability to observe closely and focus deeply.\nYou’re a fire that glows softly and burns long rather than flaring up, so your true worth shows over time. Even people who didn’t notice you at first **come to rely on you more the better they know you**, and that trust becomes your greatest strength.',
    '큰 산처럼 **묵직하고': 'Like a great mountain, you’re **grounded and dependable.** You don’t get shaken easily, and you keep everyone centered when things get chaotic.\nYou show it through actions more than words, so you might seem a little reserved at first, but once people know you, you’re **the most loyal person around.** You don’t let go of the people you care about, and you quietly stay by their side in hard times.\nBut since mountains don’t move on their own, getting started on change can take a while. **Practice carving out small paths**, and you’ll become someone who’s both solid and flexible.',
    '너른 들판처럼 **사람과': 'Like a wide-open field, you have **the power to nurture people and projects.** You’re thoughtful and detail-oriented, and nothing small slips past you.\nYou may look easygoing, but you’re smart and **know exactly what’s worthwhile.** You can sense where things will grow and where to plant the seeds, then patiently bring them to harvest.\nBut while you help others grow, you sometimes forget to take care of yourself. **Make time to give yourself water and sunlight too**, and your field will grow even richer.',
    '무쇠처럼 **단단하고 결단력': 'Like solid iron, you’re **strong and decisive.** You know right from wrong, and you don’t beat around the bush.\nYou value loyalty, so once someone is in your circle, you protect them to the end. With a strong mind that **gets calmer the bigger the crisis**, you’re the first to come up with a fix when everyone else is shaken.\nBut the harder the metal, the louder the clash. **Practice adding a softer edge to your words**, and your honesty will reach more people, more warmly.',
    '보석처럼 **섬세하고 반짝이는': 'Like a gem, you have **a delicate, sparkling sense of taste.** You notice details others miss, and your standards for quality are high.\nYou’re sensitive, so you get hurt easily, but you’re the type who **shines more clearly the more you’re polished.** You spot the small differences others walk past, and you find real joy in refining them into something beautiful.\nBut your high standards can make you push yourself too hard. Just as a gem needs light to sparkle, **let yourself take in praise and rest**, and your shine will stay bright for much longer.',
    '바다처럼 **생각이 깊고': 'Like the ocean, you’re **deep-thinking and big-picture.** Rather than staying in one place, you flow widely toward new experiences and people.\nYou don’t show everything inside, which can make you seem mysterious, but you have **a huge capacity to take anything in.** You hold many people’s stories and read the currents between them, which makes you especially strong at seeing the big picture.\nBut when your thoughts spread wide, focusing on one thing can be hard. **Practice choosing one channel and letting it flow**, and your deep thinking will turn into solid results.',
    '비와 이슬처럼 **조용히': 'Like rain and dew, you have **a quiet, seeping sensitivity.** You’re quick to pick up on things and read people’s feelings well, so you often hear that you’re easy to be around.\nWith great imagination and intuition, you’re the type who **reads the unseen flow first.** You can name moods and feelings that are hard to put into words, so people let their guard down around you.\nBut holding other people’s feelings for too long can weigh you down. **Set aside clear time just for yourself**, and your sensitivity will shine for a long time without wearing you out.',
    # 중심×주변 관계 5가지
    '당신의 중심에는 **{D}의 에너지가 있고, 주변에는 {S}의 기운이 강하게': 'At your core is **{D} energy, surrounded by a strong current of {S}.** So even when you seem calm and quiet on the outside, deep inside there’s **a center that doesn’t shake easily.**\nThe mood around you, what people say, or plans that go sideways can sway you for a moment, but you always find your way back to your center.\nUnder pressure, once you’ve made up your mind, you don’t back down. You’re **the type whose focus and grit get sharper under outside pressure.**',
    '당신의 중심에는 **{D}의 에너지가 있고, 주변에도 같은': 'At your core is **{D} energy, and plenty of the same {S} energy gathers around you.** Your colors are clear, and once you pick a direction, you push forward no matter what anyone says.\nYou do fine on your own, but your energy multiplies when you’re with people on the same wavelength. That can sometimes come off as stubborn, so **learning to match your pace with others’** becomes a huge strength.\nYou bring more power than anyone when a group looks the same way, so **just keeping good teammates close** can open up your luck in a big way.',
    '당신의 중심에는 **{D}의 에너지가 있고, 주변에는 나를 키워': 'At your core is **{D} energy, wrapped in {S} energy that helps you grow.** That makes you **a deep thinker with a big capacity to learn and absorb.**\nYou’d rather understand and be convinced before you move, so you can look slow to start, but once you begin, your depth is unmatched. With supportive people and a good environment, **your talents bloom their biggest.**\nNo need to rush if results aren’t showing yet. You’re the type whose **steadily stacked learning** suddenly bursts into bloom all at once.',
    '당신의 중심에는 **{D}의 에너지가 있고, 주변에는 내가 뿜어내는': 'At your core is **{D} energy, with the {S} energy you give off spreading wide around you.** You have a big talent for **expressing what’s in your head through words, writing, and your hands.**\nYour ideas never run out and your instincts are quick, so you shine wherever a mood needs changing or something new needs making. But since you spend so much energy outward, **make sure to take time to recharge** so you can keep sparkling.\nA single thing you say or a small thing you make travels farther than you think. **A habit of recording and sharing** is the easiest way to call in luck.',
    '당신의 중심에는 **{D}의 에너지가 있고, 주변에는 내가 다루고': 'At your core is **{D} energy, with {S} energy you can handle and grow spread wide around you.** You have a strong sense of reality and **the power to make results visible.**\nYou quickly figure out what’s needed and where to put your effort, and you move practically. The more there is to do, the more you **take charge** by organizing the whole picture.\nYour energy comes alive when you make a plan and check things off one by one. Set **a goal you can see**, and you’ll get results faster than anyone.',
    # 오행별 본문 — 나무
    '**새로 시작하고 자라나려는 힘**': 'You’re overflowing with **the drive to start fresh and grow.** You put a lot of energy into making plans and moving forward, so you’re always looking for the next goal.\nYou want to be even a little better than yesterday, so learning and taking on challenges come naturally. You care about the people around you growing too, and you’re generous with encouragement and advice.\nBut because you grow so fast, **ambition can make you miss the moment to rest.** Remember that time spent deepening your roots is part of growing too. Even if it grows slowly, the tree that reaches highest is the one with the deepest roots.',
    '새로운 걸 시작할 때 **첫발을': 'When you start something new, **taking the first step can take a while.** You’ve already run through it many times in your head, but when it’s time to move, you hesitate.\nWood energy is “the power to grow,” so when it runs low, plans tend to stay stuck in your head. Instead of a big goal, choose **one tiny step you can take today.**\nAs small starts add up, everything feels much lighter, and you’ll find yourself farther along than you thought. A tree doesn’t grow overnight, but it never stops growing, not even for a day.',
    '새 프로젝트, 첫 모임처럼 **무언가를': 'Your energy comes alive **when you open something up for the first time**, like a new project or a first meetup. Sketching out a direction where there was nothing is fun for you.\nTake on the role of making plans and showing people the way. Mentoring someone and helping them grow also feeds your Wood energy.\n**Mornings** suit you best. Big decisions and new tries go much more smoothly before noon. Like a New Year’s plan or the first page of a new notebook, your luck opens up every time you begin something.',
    '**산책, 식물 키우기, 아침 시간 활용**': '**Walks, caring for plants, and making the most of your mornings** top up your Wood energy. Just spending time somewhere green can feel like new sprouts in your heart.\nStarting to learn something new helps too. Create **small “firsts”** often, like a short online class or a walk through a neighborhood you’ve never been to.\nLong, stretching movements help as well. As stiff energy loosens up, you find the strength to grow again. The closer you keep the green, the lighter and softer your mind will feel.',
    '의욕이 넘쳐서 **이것저것': 'With so much drive, it’s easy to **start a bunch of things and miss the finish line.** You start faster than anyone, but right before the end, your attention can drift elsewhere.\nBecause you’re so sure of your ideas, **you can come off as stubborn.** When opinions clash, think “how can we grow together?” before “I’m right.”\nAim to finish at least one out of every three things you start. Every finished project makes your tree stronger. Growing one thing all the way gives your next start a much sturdier footing.',
    '괜히 **조급해지고': 'If you feel **impatient and boxed in for no reason**, that’s a sign your energy has been bent. Things not going to plan might annoy you more than usual.\nWhen that happens, slow down and take time to really stretch out. A light walk or some stretching is enough to get stuck energy flowing again.\nIt’s okay to set your goals down for a while. **Your roots keep growing even while you’re standing still.** Don’t forget that a short break is preparation for your next growth spurt.',
    '모임에서 **먼저 계획을': 'In any group, you’re **the one who makes the plan and leads.** When someone needs to set things up, like a trip or a birthday surprise, all eyes naturally turn to you.\nYou genuinely cheer on your friends’ growth, so you’re their first call for advice. You don’t just listen, you’re the type to say “okay, let’s try this” and find the way with them.\nSometimes a friend needs you to **just listen** more than advise. Catch that difference, and your friendships will grow even deeper. More friends than you think found the courage to start because of you.',
    '이런 친구는 늘 새로운 걸 제안하고': 'This friend always suggests something new and **reaches out a hand so you can grow together.** Being around them makes you set your next goal without even realizing it.',
    '중요한 약속은 오전으로': 'Schedule important plans for the morning. The same task flows more easily early in the day.\nA green phone wallpaper or a small plant on your desk is all it takes.',
    # 불
    '**표현하고 드러내려는 힘**': 'You have **a strong drive to express yourself and be seen.** Your feelings and passion run hot and you react fast, so your presence is felt clearly wherever you go.\nYour charm is your honesty, saying you like what you like and you don’t like what you don’t. You have a natural gift for lifting the mood and bringing people together.\nBut fire that blazes fast also **burns out fast.** Instead of using all your energy at once, practice sharing your spark so you can stay warm for longer. Your friends already know the air around you changes when you smile.',
    '마음은 있어도 **겉으로': 'Even when you feel it, you tend to **hold back on showing it.** You feel a lot inside, but you swallow it once more before saying it out loud.\nFire energy is “the power to show yourself,” so when it runs low, your charm may not get noticed as much as it should. Even your hard work can **quietly go unseen.**\nStart by practicing saying you like something first. One small expression brightens everything around you, and that light comes right back to you. The warmth inside you is bigger than you think, and it grows the moment you let it out.',
    '발표, 기록, 콘텐츠처럼': 'Your energy comes alive **when you put yourself out there**, like presenting, journaling, or making content. The moment you take a thought out of your head and share it, your energy multiplies.\nDon’t hesitate when it’s time to stand in front of people or change the mood. Your passion spreads to those around you fast.\n**High noon** suits you best. Try important conversations and new challenges in the daytime. You’re the type whose energy grows in front of people, so we recommend stepping onto small stages often.',
    '**햇볕 쬐기, 땀 나는 운동': '**Soaking up sunlight, working up a sweat, and seeing people you love** top up your Fire energy. Every time your body warms up, the spark in your heart comes back to life too.\nBright lighting and warm-colored clothes help as well. Just making your room a little brighter can change your mood.\nGo see shows and exhibitions you love, and feel **that flutter of excitement** often. Experiences that warm your heart are the best fuel for Fire energy. Make a point of doing something that gets your heart racing once a week. That’s the surest recharge.',
    '감정이 빨리 달아오르는': 'Because your feelings heat up fast, there are moments when **your words come out first.** Something said in the heat of the moment can stick around longer than you think.\nAlso watch out for the pattern of jumping into lots of things at once and then **suddenly burning out.** A fire that glows softly and burns long goes farther than one that flares and dies.\nWhen you’re angry, don’t reply right away. Take a beat. Drink a glass of water, wait ten minutes, and you’ll have a completely different answer. Once you learn to pace your passion, your fire will keep people warm longer than anyone’s.',
    '웃음이 줄고 **아무것도': 'If you’re laughing less and **don’t feel like doing anything**, that’s a sign your spark is fading. Things you used to love feel meh, and seeing people feels like a chore.\nYou don’t have to force yourself to act cheerful. Take a short walk in the sun or eat something warm, and start by warming up your body.\nA long chat with someone you love is the fastest recharge. Around **people who make you laugh**, your spark comes right back. A spark can shrink, but it doesn’t go out. It just needs some time sheltered from the wind.',
    '있기만 해도 **대화가': 'Just by being there, you’re **the one who brings conversations to life.** Your reactions are big and honest, so when something good happens, your friends tell you first.\nYou often break the ice and loosen up awkward moments. Plenty of friends probably became close through you.\nBut because you show your feelings so openly, **hurt feelings can show quickly too.** Add a spoonful of kindness to your honesty, and you become a friend no one can replace. On good days and hard days, yours is the first face your friends think of.',
    '이런 친구는 **밝고 솔직하게': 'This friend **lifts the mood with their bright honesty.** Being around them makes you open up the feelings you’d been hiding, without even trying.',
    '발표나 고백처럼 떨리는': 'Save nerve-racking things, like presentations or confessions, for when the sun is up.\nAdd a touch of pink somewhere small, like your lips or socks. It lifts your mood more than you’d think.',
    # 흙
    '**지키고 버티는 힘**': 'You have **great strength to protect and endure.** You don’t get shaken easily and you’re very responsible, so many people trust and lean on you.\nYou finish what you take on and you treasure your promises. You keep things steady even when situations change fast, so you become the group’s solid support.\nBut because your center of gravity is so solid, **it can take you a while to get moving.** Sometimes it’s good to move before you overthink. Wherever you are becomes a place where people can rest easy.',
    '에너지가 이리저리 흩어지기': 'Your energy scatters easily. You want to do so many things, but there are moments when you’re **unsure where to plant your feet.**\nEarth energy is “the power to hold things up,” so when it runs low, your daily rhythm wobbles and your mind can float away.\nWith **a regular routine and a place to rest**, your center gets much steadier. One small habit at the same time every day brings a big sense of stability. Once your footing is firm, the things you want to do will fall into place one by one.',
    '매일 조금씩 이어 가는 **루틴과': 'Your energy comes alive through **routines and records** you keep up a little each day. Even if the change isn’t visible, the time you’ve stacked up will never betray you.\nConnecting people and projects, and mediating between them, suits you well too. Teams last longer because you keep the balance between different opinions.\nDon’t rush big decisions — **let them sit for a while** first. The slower the conclusion, the stronger and longer it holds. One habit kept up over time becomes a weapon no one else can match.',
    '**규칙적인 식사와 잠': '**Regular meals and sleep, and a tidy space** top up your Earth energy. Just taking care of the basics can make your mind surprisingly calm.\nCooking, ceramics, or repotting plants — **hands-on making** — helps too. What you feel at your fingertips gathers scattered energy into one place.\nWalking on dirt paths or sitting on a park bench for a while is also recommended. The feeling of your feet on the ground helps you find your center again. The more firmly you take care of the basics, the more room your heart has to hold others.',
    '익숙한 걸 지키려다': 'Holding on to the familiar, you may **be slow to accept change.** Because you love stability, you might put off new things and miss chances.\nAlso watch out for the habit of **putting your own feelings last** while caring for others. If you keep saying it’s all fine, hurt can quietly pile up inside.\nNow and then, make a choice that wasn’t in the plan. Unexpected chances open up on roads you’ve never taken. Add new experiences to your steady strength, and your land will grow much wider and richer.',
    '**모든 걸 혼자 짊어지고': 'If it feels like **you’re carrying everything alone**, it’s time to rest. Your sense of responsibility might be keeping you from showing that you’re struggling.\nFeeling heavy or having trouble digesting is also a sign your Earth energy is worn out. Take care of your body first with a warm, simple home-cooked meal.\nRemember that asking for help is a skill too. **People who know how to lean on others** end up supporting others longer. The world won’t fall apart if you rest for a bit. It’ll be waiting for an even stronger you.',
    '**말없이 곁을 지켜 주는': 'You’re **the one who quietly stays by people’s side.** You keep your promises and you never change, so the longer people know you, the more they see your worth.\nWhen a friend is struggling, instead of grand words, you’re the type to buy them a meal or show up at their door. Lots of friends lean on that quiet kindness.\nNow and then, **share your own story first.** More friends than you think are curious about you, the one who always listens. Someone you’re more grateful for the longer you know them — that’s how your friends remember you.',
    '이런 친구는 **언제 연락해도': 'This friend is **there whenever you reach out.** Being around them calms a restless mind.',
    '낯선 곳보다 자주 가는': 'You’re the type who gets more done at a familiar neighborhood café than somewhere new.\nA small daily routine, like drinking tea from the same mug every morning, helps hold on to your luck.',
    # 금
    '**정리하고 결단하는 힘**': 'You have **a strong power to organize and decide.** Your standards are clear and you know when to draw the line, so you can neatly sort out even complicated situations.\nYou’re sensitive to right and wrong, and you value promises and principles. Because of that, people often trust you as “someone whose word you can count on.”\nBut with standards that sharp, it’s easy to **be too hard on yourself.** Every now and then, tell yourself it’s okay not to be perfect. Thanks to you keeping your principles, the people around you grow stronger too.',
    '결정을 미루거나 **거절을': 'You might put off decisions or **find it hard to say no.** While you’re helping with other people’s requests, your own work can get pushed back.\nMetal energy is “the power to draw a line,” so when it runs low, the line between what you need to do and what you don’t can blur.\nIt helps to set your standards ahead of time and practice saying “this is my limit.” **A clear line actually makes relationships easier.** Drawing a line isn’t cold — it protects both you and the other person.',
    '흩어진 걸 **정리하고 끝맺는': 'Your energy comes alive when you’re **organizing and finishing** scattered things. You’re brilliant at turning tangled schedules and messy information into something clear at a glance.\nTake on the role of setting standards and making the call, and your presence grows instantly. When everyone hesitates, you’re the one who says “let’s go with this.”\n**Evenings around sunset** suit you best — perfect for wrapping up the day and planning what’s next. A reputation for clean finishes brings you bigger chances as time goes on.',
    '**책상 정리, 계획표 쓰기': '**Tidying your desk, writing out plans, and clearing out things you don’t use** top up your Metal energy. When your space gets clean, your head clears too.\nWearing one shiny accessory helps as well. **Something solid and bright**, like a ring or a watch, keeps your energy neat and composed.\nDeep-breathing workouts and walks in fresh air are recommended too. The deeper your breath, the clearer your judgment. New chances always come into the space you clear. The more you tidy, the clearer your luck gets.',
    '기준이 높아서 **나와 남에게': 'With such high standards, there are moments when you **get sharp with yourself and others.** Remember that precise words can sometimes sound cold.\nOnce you decide something’s not right, you tend to **close the door on it quickly.** Before you reach a conclusion, hear the other person out one more time.\nPractice allowing “this is good enough” instead of perfection. Sometimes a slightly duller blade protects more. Strength with a touch of softness becomes trust people remember for a long time.',
    '사소한 일에도 **예민하고': 'If you’re **edgy and on edge over small things**, that’s a sign your energy has overheated. Things you’d usually let slide make your tone sharp, and you want to be alone.\nInstead of pushing yourself to see people, take some quiet time to sort things out alone. Tidying your room or journaling can be more comforting than you’d think.\nIf your chest feels tight, start by **breathing slowly and deeply.** When your breath loosens, your mind does too. Even a sharp blade gets honed again while it rests. Quiet time makes you shine even brighter.',
    '**정확하고 공정한 사람**': 'You’re **precise and fair.** You say what needs to be said rather than what sounds nice, and you always have your people’s backs.\nWhen a friend opens up, you calmly sort out the situation instead of getting swept up in feelings, so you often hear “my head feels so much clearer.”\nBut your advice can sometimes **sound like the only right answer and sting.** Before offering a fix, try saying “that must have been so hard” first. A friend who says exactly the right thing at the right moment — that’s your biggest charm.',
    '이런 친구는 **흐릿한 고민을': 'This friend **turns blurry worries into clear answers.** Being around them helps you finally make the decisions you’ve been putting off.',
    '미뤄 둔 결정은 저녁에': 'Make the decisions you’ve been putting off in the evening. It’s the time of day for wrapping up, so your judgment gets clearer.\nOne silver accessory, like a ring or watch, and a lime accent on your nails is all you need.',
    # 물
    '**생각하고 흡수하는 힘**': 'You have **a strong power to think and absorb.** You’re deeply sensitive and quick-minded, the type who has a lot going on inside more than on the outside.\nYou’re great at reading the flow, so you quickly notice small changes others miss. Your ability to blend in naturally with anyone is a big strength too.\nBut because you think so deeply, **your worries can run deep too.** Every now and then, let the thoughts circling in your head flow out through writing or talking. Because you think so deeply, you find answers a step ahead of everyone else.',
    '쉬지 않고 달리다 **생각을': 'Running nonstop, it’s easy to **miss the chance to sort out your thoughts.** You’re fine while you’re busy, but the moment you stop, all the tiredness hits at once.\nWater energy is “the power to stay and soak in,” so when it runs low, you can rush past your feelings without really feeling them.\nEven ten minutes alone a day tops up your energy. Think of **time spent doing nothing** as a must-have on your schedule. Water only gets clearer when it can pause and pool, and your heart grows deeper the same way.',
    '공부, 리서치, 대화처럼 **깊게': 'Your energy comes alive when you’re **understanding things deeply**, like studying, researching, or talking. The deeper you dig into one thing, the more you find answers others can’t see.\nReading the flow and building strategies suits you especially well. Your real skill shows when you watch the board from one step back, not out front.\n**Quiet nights** suit you best. Try organizing ideas or having deep talks at night. Holding on to the questions others easily pass by is your greatest edge.',
    '**물 자주 마시기, 반신욕': '**Drinking plenty of water, warm baths, and time alone with your thoughts** top up your Water energy. As your body fills with water, your mind fills with ease too.\nJournaling and listening to music help a lot as well. Once your feelings have a way to flow out, your heart stays clear instead of stagnant.\nWe also recommend going somewhere **you can see water**, like the sea or a river. Just the sound of water can sort out tangled thoughts. The softer your heart gets, the more smoothly your thoughts flow, and stuck things start to loosen naturally.',
    '생각이 많아서 **걱정이': 'With so much on your mind, there are times when **one worry leads to another.** You can wear yourself out imagining things that haven’t even happened yet.\nGoing along with the mood, you may **end up hiding how you really feel.** Be careful not to drift along with everyone else and forget where you actually want to go.\nWhen a worry drags on, get moving to break the loop. Even a light walk gets stagnant thoughts flowing again. The more you let your thoughts out, the clearer and deeper your water will become.',
    '**잠이 늘거나 혼자': 'If **you’re sleeping more or want to hide away**, that’s a sign your heart is tired. Even replying to messages feels like too much, and everything can feel blurry.\nInstead of forcing yourself to push through, rest deeply. Soaking in warm water or going to bed early is enough to fill your energy back up.\nWater may pool for a while, but it always flows again. **Don’t blame yourself for resting** — fill up fully, then flow again. Well-rested water can flow farther and stronger than before.',
    '**이야기를 끝까지 들어': 'You’re **the one who listens all the way to the end.** You read people’s hearts quickly, so you’re known as the friend who gets it without being told.\nYou get along with anyone and take in any story without judgment, so friends often tell you things they can’t say anywhere else.\nBut taking in others’ feelings so well can **wear you out.** As much as you listen, make sure you have someone to lean on too. There’s definitely a friend who feels lighter after talking with you.',
    '이런 친구는 **말하지 않아도': 'This friend **understands how you feel without you saying a word.** Being around them makes the worries you’ve been clutching melt away.',
    '생각 정리는 밤에': 'Sort out your thoughts at night. Even things that got tangled during the day show a way forward when you look again at night.\nCarry a tumbler and sip water often — that’s the easiest lucky routine of all.',
}

def apply():
    global s
    miss = []
    for a, b in CODE:
        if a in s: s = s.replace(a, b)
        elif b not in s: miss.append(a[:70])
    # 조각 단위 (뒤에서부터 바꿔 위치가 어긋나지 않게)
    pieces = []
    for m in re.finditer(r'<script[^>]*>(.*?)</script>', s, re.S): pieces += scan(m.group(1), m.start(1))
    left = []
    for p in sorted(pieces, key=lambda x: -x['start']):
        t = p['text']; raw = t
        key = t.replace('\\n', '\n')
        en = PIECES.get(key)
        if en is None:
            for k, v in PREFIX.items():
                if key.startswith(k): en = v; break
        if en is None: left.append(t); continue
        if '\\n' in raw: en = en.replace('\n', '\\n')
        if p['kind'] == 'tpl': en = en.replace('`', '\\`').replace('${', '\\${')
        s = s[:p['start']] + en + s[p['end']:]
    # 글꼴: Pretendard → SF Pro (시스템) · 웹폰트 Pretendard 제거
    s = re.sub(r'@font-face\{font-family:Pretendard;[^}]*\}', '', s)
    s = s.replace('--font-body:"Pretendard", -apple-system, BlinkMacSystemFont, system-ui, sans-serif', '--font-body:-apple-system, BlinkMacSystemFont, "SF Pro", "SF Pro Text", "Inter", "Helvetica Neue", Arial, sans-serif')
    s = s.replace("'ZEN SERIF','Pretendard',serif", "'ZEN SERIF',-apple-system,serif").replace('ZEN SERIF,Pretendard,serif', 'ZEN SERIF,-apple-system,serif')
    s = re.sub(r'font-family:\s*Pretendard\b[^;}]*', 'font-family:var(--font-body)', s)
    open(P_, 'w', encoding='utf-8').write(s)
    korean_left = [t for t in left if re.search(r'[가-힣]', t)]
    print('code not found:', miss)
    print('pieces left with Korean:', len(korean_left))
    for t in korean_left: print('  ', t[:100].replace('\n', '⏎'))
    print('Pretendard mentions left:', s.count('Pretendard'))
apply()
