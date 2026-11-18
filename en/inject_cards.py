# 영문 카드 그림을 chiring/index.html 속 같은 그림(base64) 자리에 넣고, '…부처의 기운' 제목 그림 대신 같은 자리의 ZEN SERIF 글자를 쓰게 함
# 사용: python3 en/make_cards_en.py && python3 en/inject_cards.py   (다시 실행해도 안전)
import base64, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = f'{D}/chiring/index.html'; s = open(P, encoding='utf-8').read()
KO = f'{D}/en/chiring_img/ko'; EN = f'{D}/en/chiring_img/en'
n = 0
for f in sorted(os.listdir(EN)):
    old = base64.b64encode(open(f'{KO}/{f}', 'rb').read()).decode()
    new = base64.b64encode(open(f'{EN}/{f}', 'rb').read()).decode()
    if old in s: s = s.replace(old, new); n += 1
    elif new in s: n += 1
    else: raise SystemExit('not found: ' + f)
a = 'n=Et(`need-title-${me}`)'
if a in s: s = s.replace(a, 'n=null')
assert 'n=null' in s
open(P, 'w', encoding='utf-8').write(s)
print('cards', n)
