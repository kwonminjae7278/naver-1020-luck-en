# 주파수 카드 그림 속 한글 글씨 → 영문 글씨
#  1) OCR로 찾은 글씨 줄 안에서 '글씨 색'에 가까운 픽셀만 골라(겹친 불꽃·클로버 등은 그대로) 주변 색으로 메움
#  2) 같은 자리·같은 색·비슷한 글꼴 성격으로 영문 카드 이름을 다시 씀 (3배 해상도 그대로)
# 사용: python3 en/make_cards_en.py  → en/chiring_img/en/*.webp
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f'{HERE}/tools')
from erase import ocr, HANG, harmonic_fill
KO = f'{HERE}/chiring_img/ko'; EN = f'{HERE}/chiring_img/en'
os.makedirs(EN, exist_ok=True)
F = '/Library/Fonts/SF-Pro-Display-{}.otf'
SUP = '/System/Library/Fonts/Supplemental/'
ZEN = os.path.expanduser('~/Library/Fonts/ZEN-SERIF-TTF-Regular.ttf')

# 카드: 영문 줄, 글꼴, 정렬, 크기 배율(한글 글씨 묶음 높이 대비), 줄 간격
CARDS = {
    'earth-1': dict(lines=['Calm', 'Down', 'First'], font=F.format('Regular'), al='C', lh=1.0, wf=1.45),
    'earth-3': dict(lines=['Stack', 'It Up'], font=F.format('Regular'), al='C', lh=1.02),
    'fire-2':  dict(lines=['Burn It', 'While You', 'Chill'], font=F.format('Regular'), al='C', lh=1.0),
    'fire-3':  dict(lines=['10,000-Calorie', 'Burn'], font=ZEN, al='C', lh=1.08),
    'metal-1': dict(lines=['Work Less,', 'Earn More'], font=F.format('Regular'), al='C', lh=1.08),
    'metal-2': dict(lines=['Wallet-', 'Closing', 'Frequency'], font=F.format('Medium'), al='C', lh=1.02, wf=1.55),
    'water-1': dict(lines=['BLAST', 'THE', 'PAST'], font=F.format('Black'), al='L', lh=.98, wf=1.2),
    'water-2': dict(lines=['Don’t Text,', 'Just Sleep'], font=SUP + 'Bodoni 72.ttc', idx=2, al='C', lh=1.08),
    'water-3': dict(lines=['New Faces', 'Incoming'], font=F.format('Regular'), al='C', lh=1.05),
    'water-5': dict(lines=['Cool-Down', 'Frequency'], font=F.format('Regular'), al='C', lh=1.05),
    'wood-1':  dict(lines=['Fresh Start,', 'Fully', 'Charged'], font=F.format('Medium'), al='C', lh=1.0, wf=1.5),
    'wood-3':  dict(lines=['Sprouting', 'a Pass'], font=F.format('Semibold'), al='C', lh=1.05),
}

def text_px(a, box, bgc):
    """box 안에서 배경과 가장 다른 픽셀들의 색 = 글씨 색"""
    x0, y0, x1, y1 = box; r = a[y0:y1, x0:x1, :3].reshape(-1, 3)
    d = np.abs(r - bgc).sum(1); sel = r[d >= np.percentile(d, 97)]
    return np.median(sel, 0)

def build(name, cfg, preview):
    src = f'{KO}/frequency__card-{name}.webp'
    im = Image.open(src).convert('RGBA'); a = np.asarray(im).astype(float); H, W = a.shape[:2]
    lines = [b for b in ocr(src) if HANG.search(b[4]) or any(c.isdigit() for c in b[4])]
    boxes = [b[:4] for b in lines]
    # 줄마다 배경색(상자 바깥 테두리 중앙값)과 글씨 색
    mask = np.zeros((H, W), bool); cols = []
    for x0, y0, x1, y1 in boxes:
        p = 14; X0, Y0, X1, Y1 = max(0, x0 - p), max(0, y0 - p), min(W, x1 + p), min(H, y1 + p)
        ring = np.concatenate([a[Y0, X0:X1, :3], a[Y1 - 1, X0:X1, :3], a[Y0:Y1, X0, :3], a[Y0:Y1, X1 - 1, :3]])
        bgc = np.median(ring, 0); tc = text_px(a, (X0, Y0, X1, Y1), bgc); cols.append(tc)
        reg = a[Y0:Y1, X0:X1, :3]
        # 글씨 색 쪽으로 절반 이상 가까운 픽셀 (안티에일리어싱 가장자리 포함)
        t = ((reg - bgc) * (tc - bgc)).sum(-1) / max(((tc - bgc) ** 2).sum(), 1)
        mask[Y0:Y1, X0:X1] |= t > .22
    mask = nd.binary_dilation(mask, iterations=4)
    ys, xs = np.nonzero(mask); m = 24
    Y0, Y1, X0, X1 = max(0, ys.min() - m), min(H, ys.max() + m), max(0, xs.min() - m), min(W, xs.max() + m)
    sub = harmonic_fill(a[Y0:Y1, X0:X1].copy(), mask[Y0:Y1, X0:X1], iters=700)
    out = a.copy(); mm = mask[Y0:Y1, X0:X1]; out[Y0:Y1, X0:X1][mm] = sub[mm]
    base = Image.fromarray(np.clip(out, 0, 255).round().astype(np.uint8), 'RGBA')
    # 영문 글씨: 한글 글씨 묶음과 같은 가운데·비슷한 높이
    bx0 = min(b[0] for b in boxes); by0 = min(b[1] for b in boxes); bx1 = max(b[2] for b in boxes); by1 = max(b[3] for b in boxes)
    n = len(cfg['lines']); maxw = min(W * .84 if cfg['al'] == 'C' else W - bx0 - 40, (bx1 - bx0) * cfg.get('wf', 1.06))
    fontp = cfg['font']; idx = cfg.get('idx', 0)
    def font(sz): return ImageFont.truetype(fontp, sz, index=idx)
    # 높이 기준 크기 → 폭이 넘치면 줄임
    target_h = (by1 - by0) * (1.0 if n >= len(boxes) else .92)
    size = 40
    while True:
        f = font(size); asc, desc = f.getmetrics(); cap = f.getbbox('H')[3] - f.getbbox('H')[1]
        lh = cap * 1.0 + size * .30 * cfg['lh'] + (cap * (cfg['lh'] - 1))
        h = cap + lh * (n - 1); w = max(f.getlength(l) for l in cfg['lines'])
        if h > target_h or w > maxw: size -= 1; break
        size += 1
    f = font(size); cap = f.getbbox('H')[3] - f.getbbox('H')[1]
    lh = cap + size * .30 * cfg['lh'] + cap * (cfg['lh'] - 1)
    h = cap + lh * (n - 1); cy = (by0 + by1) / 2
    # 줄 색: 한글 줄 색을 위에서부터 나눠 씀 (줄 수가 다르면 비율로)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    hoff = f.getbbox('H')[1]
    for i, l in enumerate(cfg['lines']):
        c = cols[min(len(cols) - 1, int(i * len(cols) / n))]
        top = cy - h / 2 + i * lh - hoff
        w = f.getlength(l)
        x = (W - w) / 2 if cfg['al'] == 'C' else bx0
        dr.text((x, top), l, font=f, fill=tuple(int(v) for v in c) + (255,))
    res = base.copy(); res.alpha_composite(lay)
    res.save(f'{EN}/frequency__card-{name}.webp', quality=92, method=6)
    preview.append((name, im, res))
    return size

if __name__ == '__main__':
    only = sys.argv[1:]
    pv = []
    for k, v in CARDS.items():
        if only and k not in only: continue
        print(k, build(k, v, pv))
    S = Image.new('RGB', (len(pv) * 330, 840), (128, 128, 128))
    for i, (n, a, b) in enumerate(pv):
        S.paste(a.convert('RGB').resize((326, 412), Image.LANCZOS), (i * 330, 4))
        S.paste(b.convert('RGB').resize((326, 412), Image.LANCZOS), (i * 330, 424))
    S.save('/private/tmp/claude-501/-Users-kwonminjae/031a7163-f030-4eb1-9b42-86dfc89f94b3/scratchpad/cards_en.jpg', quality=90)
