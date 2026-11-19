# 영문판 이미지·글자 층 만들기
#  1) 한글이 든 이미지: 한국어 원본(KO_IMG)에서 한글만 지워 img/에 저장
#  2) en/src_base.html(문구·글꼴만 영어로 바꾼 상태) + 글자 층 → src.html
# 사용: python3 en/make_en.py && python3 build.py
import os, re, sys, shutil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from erase import erase, ocr, HANG
import overlay as OV
import more as M
import numpy as np
from PIL import Image, ImageFilter
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KO_IMG = os.path.expanduser('~/Documents/네이버_chring!/02_디자인·시안/네이버_1109_치링_시나리오1화면/repo/img')
IMG = f'{D}/img'
files = {os.path.splitext(f)[0]: f for f in os.listdir(KO_IMG)}

def er(name, region=None, extra=(), skip=(), boxes=None, pad=3):
    src = f'{KO_IMG}/{files[name]}'; out = f'{IMG}/{files[name]}'
    if boxes is None:
        bx = [(x0, y0, x1, y1) for x0, y0, x1, y1, t in ocr(src) if HANG.search(t) and not any(s in t for s in skip)]
        if region: bx = [b for b in bx if b[0] >= region[0] and b[1] >= region[1] and b[2] <= region[2] and b[3] <= region[3]]
    else: bx = list(boxes)
    erase(src, out, boxes=bx + list(extra), pad=pad)
    return bx

s = open(f'{D}/en/src_base.html', encoding='utf-8').read()
def ov(name, frame, rect, origin, drop=False, **kw):
    global s
    s = OV.insert(s, name, OV.build(frame, rect, origin, **{k: v for k, v in kw.items() if k in ('em_color', 'overrides', 'skip', 'only', 'extra', 'nowrap')}), drop_img=drop)

# ── Lucky Item · Place · Music ──
for key, frame, em in (('item', 'Lucky Item', '#d1ff69'), ('place', 'Lucky Place', '#5effc7'), ('music', 'Lucky Music', '#13e2ff')):
    er(f'n_{key}_head', region=(60, 55, 402, 112)); ov(f'n_{key}_head', frame, (0, 55, 402, 112), (0, 0))
    ov(f'n_{key}_body', frame, (20, 505, 382, 570), (20, 505), drop=True, em_color=em)
    er(f'n_{key}_icons'); ov(f'n_{key}_icons', frame, (14, 605, 388, 745), (14, 605))
    er(f'n_{key}_btn'); ov(f'n_{key}_btn', frame, (14, 778, 388, 850), (14, 778))

# ── 운세 겹쳐보기 결과 카드 3장 (장소 = Figma 'Mix Place', 아이템·플리 = 같은 틀에 영문 문구) ──
MP = OV.FIG['Mix Place']
def mp(t): return next(i for i in MP if i[0] == t)
def clone(it, text, x=None, w=None, segs=None):
    n = list(it); n[0] = text
    if x is not None: n[1] = x
    if w is not None: n[3] = w
    n[6] = segs or [[len(text)] + list(it[6][-1][1:])]
    return n
def body(text, word):
    i = text.index(word); j = i + len(word); b = mp(MP[0][0])[6]
    return clone(mp(MP[0][0]), text, segs=[[i] + b[0][1:], [j] + b[1][1:], [len(text)] + b[2][1:]])
def cx(t, center, size=16, wt=600, ls=-4):
    w = M.width(t, size, 'SF', wt, size * ls / 100); return center - w / 2, w
ICX = [mp('Confidence UP')[1] + mp('Confidence UP')[3] / 2, mp('Easygoing')[1] + mp('Easygoing')[3] / 2, mp('Wood Vibe')[1] + mp('Wood Vibe')[3] / 2]
SHX = mp('Share Place')[1] + mp('Share Place')[3] / 2
for key, head, bt, word, icons, share in (
        ('mxi', 'Today’s Lucky Item', 'Fill up on the Earth energy you need with a cozy beige. Wrap a muffler around you and hold your wavering heart steady.', 'Earth energy',
         ('Stability UP', 'Calm Day', 'Earth Vibe'), 'Share Item'),
        ('mxm', 'Today’s Lucky Playlist', 'Fill up on the Water energy you need with songs as gentle as rain. Let a softly worded track carry your tangled thoughts away.', 'Water energy',
         ('Focus UP', 'Calm Mind', 'Water Vibe'), 'Share Playlist')):
    hd = mp('Today’s Lucky Place'); x, w = cx(head, 201, 20, 600, -1)
    items = [clone(hd, head, x, w), body(bt, word)]
    for t, c in zip(icons, ICX):
        x, w = cx(t, c); items.append(clone(mp('Easygoing'), t, x, w))
    x, w = cx(share, SHX, 20, 600, -2); items.append(clone(mp('Share Place'), share, x, w)); items.append(mp('Got it'))
    OV.FIG[key] = items
for key, frame, em in (('mapo', 'Mix Place', '#5effc7'), ('mxi', 'mxi', '#1ecde7'), ('mxm', 'mxm', '#e892e0')):
    er(f'n_{key}_head', region=(60, 55, 402, 112)); ov(f'n_{key}_head', frame, (0, 55, 402, 112), (0, 0))
    ov(f'n_{key}_body', frame, (0, 505, 402, 570), (20, 505), drop=True, em_color=em)
    er(f'n_{key}_icons'); ov(f'n_{key}_icons', frame, (14, 605, 388, 745), (14, 605))
    er(f'n_{key}_ok'); ov(f'n_{key}_ok', frame, (14, 776, 202, 846), (14, 776))
    er(f'n_{key}_share'); ov(f'n_{key}_share', frame, (202, 776, 388, 846), (202, 776))

# ── 오늘의 행운 담기 (카메라): 장소 칩의 핀 아이콘을 영문 글자 길이에 맞춰 왼쪽으로 ──
er('n_cam_base', region=(0, 50, 402, 874), skip=('하우스',))
M.move_patch(f'{IMG}/n_cam_base.jpg', (121, 146, 138, 172), -14, fill_boxes=[(140, 146, 280, 172)])
ov('n_cam_base', 'Cam', (0, 50, 402, 874), (0, 0))

# ── 장소 인증 Charm ──
er('n_charm_bg', region=(0, 50, 402, 874)); ov('n_charm_bg', 'Charm', (0, 50, 402, 770), (0, 0))
er('n_charm_btn'); ov('n_charm_btn', 'Charm', (0, 778, 402, 850), (14, 778))

# ── 인증 결과 ──
ov('n_res_title', 'Result', (0, 130, 402, 230), (14, 135), drop=True, overrides={'Your Water energy\nis fully charged': {'w': 340}})
ov('n_res_sub', 'Result', (0, 505, 402, 580), (60, 505), drop=True)
s = s.replace('font-size:24px;letter-spacing:-1.92px', 'font-size:24px;letter-spacing:-0.48px', 1)   # 영문은 -8%가 너무 붙어 보여 -2%로
er('n_res_tiles'); ov('n_res_tiles', 'Result', (14, 620, 388, 745), (14, 620))
er('n_res_btn'); ov('n_res_btn', 'Result', (0, 778, 402, 850), (14, 778))

# ── 오늘의 행운 모아보기 ──
er('c_head')
s = OV.insert(s, 'c_head', M.T('All your luck\nfor today, in one place', 21, 134.5, 28, wt=600, al='L', ls_pct=-4, lh_pct=140))
er('c_btn'); s = OV.insert(s, 'c_btn', M.T('Got it', 187, 35, 20, wt=600, color=M.text_color(f'{KO_IMG}/c_btn.png', (150, 20, 225, 50)), ls_pct=-2, lh_pct=120))

# ── 키링 완성 ──
ov('n_key_title', 'Keyring', (0, 100, 402, 200), (14, 108), drop=True, overrides={'Your lucky keyring is ready!': {'text': 'Your lucky keyring\nis ready!', 'w': 340}})
er('n_key_btns'); ov('n_key_btns', 'Keyring', (0, 778, 402, 850), (14, 778))

# ── 홈 ──
er('n_home_base', region=(0, 100, 402, 400), extra=[(130, 114, 270, 143)])
pill_w = M.width('Save Today’s Luck', 15, 'SF', 700, -.15) + 32
px0, px1 = M.widen(f'{IMG}/n_home_base.jpg', (136, 356, 266, 396), pill_w)
ov('n_home_base', 'Home', (0, 100, 402, 420), (0, 0), overrides={'Save Today’s Luck': {'y': 367}})
s = s.replace('id="ctaCapture" role="button" aria-label="Save Today’s Luck" style="left:136px;top:356px;width:130px;',
              f'id="ctaCapture" role="button" aria-label="Save Today’s Luck" style="left:{px0}px;top:356px;width:{px1 - px0}px;')

# ── 운세 도착 딤 (홈을 23px 아래로 내리고 어둡게 한 그림 + 열쇠 카드) ──
# 홈 부분은 영문 홈 배경(글자를 지운 것)으로 다시 만들고, 그 위에 같은 비율로 어둡게 한 영문 글자, 맨 위에 원래 카드 층을 다시 얹음
from scipy import ndimage as nd
DK, DB = .2014, 2.775
def dimc(c):
    c = c.lstrip('#'); a = c[6:8]
    rgb = [round(DK * int(c[i:i + 2], 16) + DB) for i in (0, 2, 4)]
    return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{int(a, 16) / 255:.3f})' if a else '#%02x%02x%02x' % tuple(rgb)
hk = np.asarray(Image.open(f'{KO_IMG}/n_home_base.jpg').convert('RGB')).astype(float)
he = np.asarray(Image.open(f'{IMG}/n_home_base.jpg').convert('RGB')).astype(float)
HOME = OV.FIG['Home']
for n in ('n_dim1', 'n_dim2'):
    d = np.asarray(Image.open(f'{KO_IMG}/{n}.jpg').convert('RGB')).astype(float)
    pk = np.full_like(d, 6.0); pk[23:] = DK * hk[:-23] + DB
    pe = np.full_like(d, 6.0); pe[23:] = DK * he[:-23] + DB
    diff = np.abs(d - pk).max(-1)
    m = np.zeros(diff.shape, bool); m[128:503] = diff[128:503] > 6
    m = nd.binary_fill_holes(nd.binary_closing(m, iterations=3))
    lab, k = nd.label(m); sz = nd.sum(m, lab, range(1, k + 1)); m = np.isin(lab, 1 + np.nonzero(sz > 2000)[0])
    out = d.copy(); band = np.zeros_like(m); band[128:503] = True
    out[band & ~m] = pe[band & ~m]
    Image.fromarray(out.round().astype(np.uint8)).save(f'{IMG}/{n}.jpg', quality=96, subsampling=0)
    # 카드 층 (가장자리 1px 부드럽게)
    al = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))).astype(float)
    al[503:] = 0
    card = np.dstack([d, al]).round().astype(np.uint8)
    Image.fromarray(card, 'RGBA').crop((0, 0, 402, 503)).save(f'{IMG}/{n}_card.png', optimize=True)
    # 아래쪽: 옆 카드 부제·내비 글자 지우기
    erase(f'{IMG}/{n}.jpg', f'{IMG}/{n}.jpg', boxes=[(0, 578, 66, 622), (337, 578, 402, 622), (40, 826, 72, 849), (122, 826, 180, 846), (222, 826, 266, 849), (324, 826, 358, 846)], pad=1)
    inner = ''
    for it in HOME:
        if 100 < it[2] < 300:
            inner += OV.text_html(it, 0, -23, override={'color': dimc(it[6][0][6])})
    sc = M.text_color(f'{KO_IMG}/{n}.jpg', (340, 580, 386, 600))
    clip = 'clip-path:inset(0 0 0 {}px)'
    inner += M.T('Today’s tracks that\ncharge your luck', 263.2, 589.5, 14.4, wt=600, al='L', ls_pct=-2.5, lh_pct=138, color=sc, extra='clip-path:inset(-4px -4px -4px 72px)')
    inner += M.T('Today’s spot\nto bring you luck', -30.8, 589.5, 14.4, wt=600, al='L', ls_pct=-2.5, lh_pct=138, color=sc, extra='width:160px;clip-path:inset(-4px 62px -4px -4px)')
    for t, cx_, box in (('Home', 56, (46, 828, 66, 846)), ('Archive', 151, (126, 828, 176, 844)), ('Friends', 244, (224, 828, 264, 848)), ('Energy', 341, (326, 828, 356, 844))):
        col = M.text_color(f'{KO_IMG}/{n}.jpg', box)
        inner += M.T(t, cx_, 837, 13, wt=600 if t == 'Home' else 400, ls_pct=-0.5, color=col)
    inner += f'<img class="en-bg" src="__img_{n}_card__" alt="" draggable="false" style="height:503px;bottom:auto">'
    s = OV.insert(s, n, inner)

# ── 친구방 ──
er('n_fr_head', region=(0, 50, 402, 104)); ov('n_fr_head', 'Friends', (0, 50, 402, 104), (0, 0))
er('n_fr_top'); ov('n_fr_top', 'Friends', (0, 104, 402, 653), (0, 104))

# ── 행운 공구방 (채팅) 머리: 제목이 길어진 만큼 클로버·인원수를 오른쪽으로 ──
title_w = 124.7   # 브라우저에서 잰 실제 폭 (SF Pro 22 · 600 · -2%)
for name, frame in (('n_chat_head', 'ChatDone'), ('n_rank_panel', 'Rank'), ('n_chat_bg', 'ChatDone')):
    src = f'{IMG}/{files[name]}'
    er(name, region=(0, 50, 402, 874), skip=('공구방',))
    M.move_patch(src, (238, 66, 281, 100), round(137 + title_w + 5 - 240), fill_boxes=[(133, 66, 237, 100)])
    if name != 'n_chat_bg':
        ov(name, frame, (0, 60, 402, 175), (0, 0), skip=('sumin', 'Dayun', 'Yujin'))
er('n_chat_input')
s = OV.insert(s, 'n_chat_input', M.T('Leave a message', 44, 43, 16, wt=400, al='L', ls_pct=-3,
              color=M.text_color(f'{KO_IMG}/n_chat_input.jpg', (40, 30, 175, 56))))

# 채팅 말풍선: 한글 말풍선을 지우고, 같은 자리·같은 모양의 실제 말풍선(영문 길이에 맞춘 폭)으로
CHAT = {
    'n_chat_msgs': ['guys tmrw’s weather 🔥', 'meet up?', 'yesss obv', 'where? Seongsu? Yongsan?', 'omg the weather’s so good', 'wait lemme ask the app lol', None],
    'n_chat_new0': ['it even picked our spot ty'], 'n_chat_new1': [None], 'n_chat_new2': ['Han River?? tmrw here?'],
    'n_chat_new3': ['spicy tteokbokki picnic?'], 'n_chat_new4': ['I’m in hehe'], 'n_chat_new5': ['see u in Mapo ~~!~!'],
    'n_chat_a': ['omg legendary, Sumin has an exam\nand got #1 luck lmao', 'isn’t this a pass spoiler?', 'ugh I’m dead last T_T', 'I’m actually spiraling',
                 'yesss my luck is insane', 'charms on me, grab one!', 'pls pls pick me, it has to be me', 'presenting today and I’m so not ready T_T'],
}
for name, texts in CHAT.items():
    src = f'{KO_IMG}/{files[name]}'; out = f'{IMG}/{files[name]}'
    bs = M.bubbles(src)
    assert len(bs) == len(texts), (name, bs)
    clear = []; inner = ''
    for b, t in zip(bs, texts):
        if t is None: continue
        if b[3] - b[1] > 44 and '\n' not in t: b[3] = b[1] + 40      # 아래 빛 번짐까지 붙어 잡힌 말풍선
        clear.append(b[:4]); inner += M.bubble_html(b, t)
    if clear: M.clear_rects(src, out, clear)
    if name == 'n_chat_msgs':      # 겹쳐보기 말풍선 (ZEN SERIF)
        erase(out, out, boxes=[(80, 400, 258, 432), (78, 432, 168, 463)], pad=3)
        inner += OV.build('ChatDone', (60, 570, 320, 680), (0, 190))
    if name == 'n_chat_new1':      # 장소 카드
        er('n_chat_new1')
        inner += OV.build('ChatDone', (240, 740, 402, 880), (0, 190 + 554))
    s = OV.insert(s, name, inner)

# ── 운세 순위 비교 ──
er('n_rk_title', skip=('공구방',))
rk_w = 124.7; grp = rk_w + 8 + 16
M.move_patch(f'{IMG}/n_rk_title.png', (184, 4, 205, 36), round(141 - grp / 2 + rk_w + 8 - 186), fill_boxes=[(62, 4, 183, 36)])
rkc = M.text_color(f'{KO_IMG}/n_rk_title.png', (78, 8, 180, 32), bg=np.array([0, 0, 0]))
s = OV.insert(s, 'n_rk_title', M.T('Lucky Squad', 141 - grp / 2, 19.5, 22, wt=600, al='L', color=rkc, ls_pct=-2)
              + M.T('Today’s lucky one?', 141, 75, 32, fam='ZEN', wt=400, ls_pct=-1))
for name in ('n_rk_bg0', 'n_rk_bg1'):
    er(name, region=(0, 780, 402, 850))
    s = OV.insert(s, name, M.T('Got it', 109, 812, 20, wt=600, color=M.text_color(f'{KO_IMG}/{files[name]}', (80, 795, 140, 830)), ls_pct=-2)
                  + M.T('Send Energy', 293, 812, 20, wt=600, color=M.text_color(f'{KO_IMG}/{files[name]}', (235, 795, 350, 830)), ls_pct=-2))

# ── 운세 겹쳐보기 결과 ──
er('n_mix_title')
mtc = M.text_color(f'{KO_IMG}/n_mix_title.png', (60, 8, 160, 30), bg=np.array([0, 0, 0]))
s = OV.insert(s, 'n_mix_title', M.T('Luck Overlap', 111, 18.5, 16, wt=500, color=mtc, ls_pct=-2)
              + M.T('What energy do\nwe need today?', 111, 74.5, 32, fam='ZEN', wt=400, ls_pct=-2, lh_pct=143))
er('n_mix_caption')
s = OV.insert(s, 'n_mix_caption', M.T('Tap a card to see more', 121, 19.5, 14, wt=500, ls_pct=-2,
              color=M.text_color(f'{KO_IMG}/n_mix_caption.png', (20, 10, 222, 30), bg=np.array([0, 0, 0]))))
er('n_mix_ok'); s = OV.insert(s, 'n_mix_ok', M.T('Got it', 95, 34, 20, wt=600, ls_pct=-2, color=M.text_color(f'{KO_IMG}/n_mix_ok.png', (70, 20, 120, 48))))
er('n_mix_share'); s = OV.insert(s, 'n_mix_share', M.T('Share Results', 90, 34, 20, wt=600, ls_pct=-2, color=M.text_color(f'{KO_IMG}/n_mix_share.png', (30, 18, 150, 50))))

# ── 키보드 (스토리 메시지): 한글 자판 → 영문 자판 (자리 배열이 같음) ──
from scipy import ndimage as nd
kim = Image.open(f'{KO_IMG}/lm_kbd.jpg').convert('RGB'); ka = np.asarray(kim).astype(int); kg = ka.mean(-1)
lab, _ = nd.label(kg > 85); keys = []
for sl in nd.find_objects(lab):
    if sl[0].stop - sl[0].start > 30 and sl[1].stop - sl[1].start > 20: keys.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop))
keys.sort(key=lambda k: (k[1], k[0]))
kout = ka.copy()
for k in keys:   # 글자 키·스페이스 키: 키 안쪽을 키 색 그대로 메움 (둥근 모서리·그림자는 그대로)
    x0, y0, x1, y1 = k; col = np.median(ka[y0 + 3:y0 + 6, x0 + 8:x1 - 8].reshape(-1, 3), 0)
    kout[y0 + 5:y1 - 5, x0 + 5:x1 - 5] = col
Image.fromarray(kout.astype(np.uint8)).save(f'{IMG}/lm_kbd.jpg', quality=96, subsampling=0)
letters = list('qwertyuiop') + list('asdfghjkl') + list('zxcvbnm')
kb = ''
for k, ch in zip(keys[:26], letters):
    kb += M.T(ch, (k[0] + k[2]) / 2, (k[1] + k[3]) / 2 - 3.5, 23, wt=400, ls_pct=0, color='#fff')
sp = keys[26]; kb += M.T('space', (sp[0] + sp[2]) / 2, (sp[1] + sp[3]) / 2, 16, wt=400, ls_pct=0, color='#fff')
s = OV.insert(s, 'lm_kbd', kb)

s = s.replace('</style>', OV.CSS + M.CSS + '</style>', 1)
open(f'{D}/src.html', 'w', encoding='utf-8').write(s)
print('ok')
