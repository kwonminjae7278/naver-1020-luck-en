# 영문판 글자 덧입히기: Figma 영문 시안(네이버_영어)의 글자 위치·크기·굵기·자간·행간·색을 그대로
# 실제 글꼴(SF Pro / ZEN SERIF)의 HTML 글자로 만들어, 글자를 지운 이미지 바로 위에 같은 모션으로 얹음
import json, os, re, html
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = {}
for f in ('figma_text.json', 'figma_text2.json', 'figma_text3.json'):
    p = f'{D}/data/{f}'
    if os.path.exists(p): FIG.update(json.load(open(p, encoding='utf-8')))

FAM = {'SF': 'var(--en-sf)', 'ZEN SERIF': "'ZEN SERIF', serif", 'Urbanist': "'Urbanist', var(--en-sf)", 'SUIT Variable': 'var(--en-sf)'}

def css_color(c):
    if not c: return '#fff'
    if len(c) == 9: return f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},{int(c[7:9],16)/255:.3f})'
    return c

def text_html(item, ox, oy, em_color=None, override=None, nowrap=None, dx=0, dy=0, cls=''):
    t, x, y, w, h, al, segs = item
    o = override or {}
    t = o.get('text', t); x = o.get('x', x); y = o.get('y', y); w = o.get('w', w); h = o.get('h', h); al = o.get('al', al)
    fam, wt, size, ls, lh, col = segs[0][1:7] if len(segs[0]) >= 7 else (None,) * 6
    big = max(segs, key=lambda s: s[0])
    fam, wt, size, ls, lh, col = segs[-1][1], segs[-1][2], segs[-1][3], segs[-1][4], segs[-1][5], segs[-1][6]
    # 가장 긴 구간의 스타일을 기본으로
    spans = []; prev = 0; lens = []
    for s in segs: lens.append((s[0] - prev, s)); prev = s[0]
    base = max(lens, key=lambda z: z[0])[1]
    fam, wt, size, ls, lh, col = base[1], base[2], base[3], base[4], base[5], base[6]
    size = o.get('size', size)
    lsv = (float(str(ls).replace('px', '')) if 'px' in str(ls) else size * ls / 100)
    lhv = f'{lh / 100:.3f}' if lh else 'normal'
    one_line = '\n' not in t and h < size * (lh / 100 if lh else 1.25) * 1.6
    nw = one_line if nowrap is None else nowrap
    st = [f'top:{y - oy + dy:.1f}px', f'font-family:{FAM.get(fam, "var(--en-sf)")}', f'font-weight:{wt}', f'font-size:{size}px',
          f'letter-spacing:{lsv:.2f}px', f'line-height:{lhv}', f'color:{css_color(o.get("color", col))}']
    if nw and al == 'C': st += [f'left:{x - ox + dx + w / 2:.1f}px', 'transform:translateX(-50%)', 'white-space:nowrap']
    elif nw and al == 'R': st += [f'right:calc(100% - {x - ox + dx + w:.1f}px)', 'white-space:nowrap', 'text-align:right']
    elif nw: st += [f'left:{x - ox + dx:.1f}px', 'white-space:nowrap']
    else: st += [f'left:{x - ox + dx:.1f}px', f'width:{w + o.get("wpad", 2):.1f}px', 'white-space:pre-line', 'text-align:' + {'C': 'center', 'R': 'right', 'L': 'left'}[al]]
    # 굵기·색이 다른 구간 (예: 강조 단어)
    body = ''; prev = 0
    if 'text' in o: body = html.escape(t)
    else:
        for s in segs:
            piece = html.escape(t[prev:s[0]]); prev = s[0]
            if s[2] != wt or s[6] != col or s[3] != size:
                c2 = css_color(em_color or s[6])
                body += f'<b style="font-weight:{s[2]};color:{c2}">{piece}</b>'
            else: body += piece
    return f'<span class="en-t{(" " + cls) if cls else ""}" style="{";".join(st)}">{body}</span>'

def build(frame, rect, origin, em_color=None, overrides=None, skip=(), only=None, extra=(), nowrap=None):
    """rect: (x0,y0,x1,y1) 이 이미지가 덮는 시안 영역, origin: 이미지 왼쪽 위의 시안 좌표"""
    ox, oy = origin; out = []
    for it in FIG[frame]:
        t, x, y, w, h = it[:5]
        cx, cy = x + w / 2, y + h / 2
        if only is not None and t not in only: continue
        if t in skip: continue
        if not (rect[0] <= cx <= rect[2] and rect[1] <= cy <= rect[3]): continue
        out.append(text_html(it, ox, oy, em_color, (overrides or {}).get(t), nowrap))
    for it, o in extra: out.append(text_html(it, ox, oy, em_color, o, nowrap))
    return ''.join(out)

def insert(src, name, inner, drop_img=False, extra_cls='', wrap_style=''):
    """__img_name__ 을 쓰는 <img>를 같은 자리·같은 속성(id·class·data·모션)의 묶음으로 바꾸고, 안에 [글자를 지운 이미지 + 실제 글자]를 넣음.
    drop_img면 이미지 없이 글자만 (글자만 있던 이미지)."""
    m = re.search(r'<img\b[^>]*__img_' + re.escape(name) + r'__[^>]*>', src)
    assert m, name
    tag = m.group(0)
    alt = re.search(r'alt="([^"]*)"', tag); alt = alt.group(1) if alt else ''
    attrs = re.sub(r'^<img\b|/?>$', '', tag)
    attrs = re.sub(r'\s(src|alt|draggable)="[^"]*"', '', attrs)
    if 'class="' in attrs: attrs = re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} en-wrap{(" " + extra_cls) if extra_cls else ""}"', attrs, 1)
    else: attrs += f' class="en-wrap{(" " + extra_cls) if extra_cls else ""}"'
    if wrap_style: attrs = re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1)};{wrap_style}"', attrs, 1)
    bg = '' if drop_img else f'<img class="en-bg" src="__img_{name}__" alt="" draggable="false">'
    new = f'<div{attrs} aria-label="{alt}">{bg}{inner}</div>'
    return src.replace(tag, new, 1)

CSS = '''
  /* ── 영문판: 이미지 위에 얹는 실제 글자 (Figma 영문 시안의 위치·크기·자간·행간 그대로) ── */
  :root { --en-sf: -apple-system, BlinkMacSystemFont, "SF Pro", "SF Pro Text", "Inter", "Helvetica Neue", Arial, sans-serif; }
  .en-t { position: absolute; pointer-events: none; margin: 0; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; font-kerning: normal; text-rendering: geometricPrecision; }
  .en-t b { font-style: normal; }
  .en-wrap > .en-bg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; pointer-events: none; }
'''
