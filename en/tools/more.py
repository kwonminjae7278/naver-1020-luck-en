# 영문판 보조 도구: Figma 영문 프레임이 없는 화면의 글자 배치, 말풍선 다시 그리기, 아이콘 옮기기, 알약 버튼 늘리기
import html, os
import numpy as np
from PIL import Image, ImageFont

SF = {400: '/Library/Fonts/SF-Pro-Text-Regular.otf', 500: '/Library/Fonts/SF-Pro-Text-Medium.otf',
      600: '/Library/Fonts/SF-Pro-Display-Semibold.otf', 700: '/Library/Fonts/SF-Pro-Display-Bold.otf'}
ZEN = os.path.expanduser('~/Library/Fonts/ZEN-SERIF-TTF-Regular.ttf')
URB = None
# 세로 글꼴 값 (em): 위쪽 높이, 아래쪽 깊이, 대문자 높이
MET = {'SF': (1950 / 2048, 494 / 2048, 1443 / 2048), 'ZEN': (1.0, .3, .756)}
FAMCSS = {'SF': 'var(--en-sf)', 'ZEN': "'ZEN SERIF', serif"}

def width(text, size, fam='SF', wt=600, ls=0.0):
    """글자 폭(px). ls는 px 단위 자간"""
    path = ZEN if fam == 'ZEN' else SF.get(wt, SF[600])
    f = ImageFont.truetype(path, 200)
    return max(f.getlength(l) * size / 200 + ls * len(l) for l in text.split('\n'))

def T(text, x, cy, size, fam='SF', wt=600, color='#fff', al='C', ls_pct=-2.0, lh_pct=None, ox=0, oy=0, extra=''):
    """한 줄(또는 여러 줄) 글자. (x, cy) = 첫 줄 대문자 높이의 가운데가 올 시안 좌표 (al C: 가운데 x, L: 왼쪽 x, R: 오른쪽 x)"""
    asc, desc, cap = MET[fam]
    L = size * (lh_pct / 100 if lh_pct else 1.25)
    top = cy - ((L - (asc + desc) * size) / 2 + asc * size - cap * size / 2)
    ls = size * ls_pct / 100
    st = [f'top:{top - oy:.2f}px', f'font-family:{FAMCSS[fam]}', f'font-weight:{wt}', f'font-size:{size}px',
          f'letter-spacing:{ls:.2f}px', f'line-height:{L:.2f}px', f'color:{color}', 'white-space:pre']
    if al == 'C': st += [f'left:{x - ox:.2f}px', 'transform:translateX(-50%)', 'text-align:center']
    elif al == 'R': st += [f'right:calc(100% - {x - ox:.2f}px)', 'text-align:right']
    else: st += [f'left:{x - ox:.2f}px']
    if extra: st.append(extra)
    return f'<span class="en-t" style="{";".join(st)}">{html.escape(text)}</span>'

def text_color(path, box, bg=None):
    """box 안 글자 색: 배경에서 가장 먼 쪽 픽셀들의 평균"""
    a = np.asarray(Image.open(path).convert('RGBA')).astype(float)
    x0, y0, x1, y1 = box; r = a[y0:y1, x0:x1].reshape(-1, 4)
    r = r[r[:, 3] > 200]
    if bg is None: bg = np.median(np.concatenate([a[y0, x0:x1], a[y1 - 1, x0:x1]])[:, :3], 0)
    d = np.abs(r[:, :3] - bg).sum(1)
    sel = r[d >= d.max() * .85]
    c = sel[:, :3].mean(0).round().astype(int)
    return '#%02x%02x%02x' % tuple(c)

def bubbles(path, min_h=30, min_w=40):
    """채팅 이미지 속 말풍선(불투명 둥근 사각형) 찾기 → [(x0,y0,x1,y1,'L'|'R', 색)]  (아바타·특수 카드 제외는 호출 쪽에서)"""
    from scipy import ndimage as nd
    a = np.asarray(Image.open(path).convert('RGBA')).astype(int)
    m = a[..., 3] > 200
    lab, n = nd.label(m)
    out = []
    for sl in nd.find_objects(lab):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if y1 - y0 < min_h or x1 - x0 < min_w: continue
        c = a[(y0 + y1) // 2, x0 + 4, :3]
        if x0 <= 22: continue   # 아바타
        side = 'R' if c.mean() > 150 else 'L'
        out.append([x0, y0, x1, y1, side, tuple(int(v) for v in c)])
    out.sort(key=lambda b: b[1])
    return out

def clear_rects(src, out, rects, pad=1):
    """투명 배경 위의 말풍선을 지움: 상자 안을 주변(옅은 빛 번짐 포함)으로 메움"""
    from erase import erase
    erase(src, out, boxes=[(x0, y0, x1, y1) for x0, y0, x1, y1 in rects], pad=pad)

def bubble_html(b, text, oy=0):
    x0, y0, x1, y1, side = b[:5]
    h = y1 - y0
    if side == 'R':
        st = f'right:{402 - x1}px;top:{y0 - oy}px;height:{h}px'
    else:
        st = f'left:{x0}px;top:{y0 - oy}px;height:{h}px'
    return f'<span class="en-bub {side}" style="{st}">{html.escape(text)}</span>'

def move_patch(path, box, dx, fill_boxes=(), out=None):
    """box 안 그림(아이콘 등)을 dx만큼 옮김. 원래 자리는 fill_boxes와 함께 주변 색으로 메움"""
    from erase import erase
    out = out or path
    im = Image.open(path).convert('RGBA')
    patch = im.crop(box)
    erase(path, out, boxes=list(fill_boxes) + [box], pad=2)
    im2 = Image.open(out).convert('RGBA')
    im2.alpha_composite(patch, (box[0] + dx, box[1]))
    save(im2, out, path)

def save(img, out, ref):
    if out.endswith('.jpg'): img.convert('RGB').save(out, quality=96, subsampling=0)
    else: img.save(out)

def widen(path, box, new_w, out=None):
    """알약 버튼(가로로 늘어나도 모양이 같은 것)을 가운데를 기준으로 new_w 폭으로 늘림: 양 끝 둥근 부분은 그대로, 가운데 세로줄을 반복"""
    out = out or path
    im = Image.open(path).convert('RGBA')
    x0, y0, x1, y1 = box; w = x1 - x0; cx = (x0 + x1) / 2
    strip = im.crop(box); half = w // 2
    left = strip.crop((0, 0, half, y1 - y0)); right = strip.crop((w - half, 0, w, y1 - y0))
    mid = strip.crop((half - 1, 0, half, y1 - y0))
    nw = int(round(new_w)); new = Image.new('RGBA', (nw, y1 - y0))
    for x in range(half, nw - half): new.paste(mid, (x, 0))
    new.paste(left, (0, 0)); new.paste(right, (nw - half, 0))
    nx0 = int(round(cx - nw / 2))
    im.paste(new, (nx0, y0))
    save(im, out, path)
    return nx0, nx0 + nw

CSS = '''
  /* 영문판 채팅 말풍선: 시안 말풍선과 같은 색·모서리·여백, 글자 길이에 맞춰 폭이 정해짐 */
  .en-bub { position: absolute; display: flex; align-items: center; box-sizing: border-box; white-space: pre; pointer-events: none;
            font-family: var(--en-sf); -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; letter-spacing: -.15px; line-height: 1.55; }
  .en-bub.L { background: #2f3034; color: #fff; font-weight: 400; font-size: 15.23px; padding: 0 14px; border-radius: 2px 10px 10px 10px; }
  .en-bub.R { background: #f0f0f0; color: #000; font-weight: 500; font-size: 15.09px; padding: 0 15px; border-radius: 14px 2px 14px 14px; }
  /* 이미지 → 묶음(div)으로 바뀐 곳도 원래 img 규칙을 그대로 받게 */
  .ch-thread .en-wrap { position: absolute; display: block; pointer-events: none; }
  .ch-thread .en-wrap.nm { opacity: 0; transform: translateY(14px) scale(.97); transform-origin: 100% 100%; transition: opacity .35s var(--ease), transform .5s var(--spring); }
  .ch-thread .en-wrap.nm.show { opacity: 1; transform: none; }
  .ch-thread > .en-wrap.thread-a { opacity: 0; visibility: hidden; transform: translateY(18px);
                              transition: opacity .3s var(--ease), transform .3s var(--ease), visibility 0s .3s, top .5s var(--ease); }
  .ch-thread > .en-wrap.thread-a.show { opacity: 1; visibility: visible; transform: none;
                              transition: opacity .45s var(--ease), transform .6s var(--spring), visibility 0s, top .5s var(--ease); }
  .fr-content > .en-wrap { display: block; position: relative; pointer-events: none; }
  #rkPanel > .en-wrap { display: block; position: relative; width: 402px; height: 292px; }
  #stKbd.en-wrap { pointer-events: none; }
'''
