# chiring 번들(JS)에서 한글이 들어간 문자열 조각을 정확히 뽑기: '..', "..", `..`(템플릿은 ${} 사이 조각 단위), /정규식/
import re, json, sys
HANG = re.compile(r'[가-힣ㄱ-ㅣ]')
def scan(js, base=0):
    out = []; i = 0; n = len(js); prev = ''
    def add(kind, a, b):
        t = js[a:b]
        if HANG.search(t): out.append({'kind': kind, 'start': base + a, 'end': base + b, 'text': t})
    def template(i):                      # js[i] == '`'
        j = i + 1; seg = j
        while j < n:
            c = js[j]
            if c == '\\': j += 2; continue
            if c == '`': add('tpl', seg, j); return j + 1
            if c == '$' and j + 1 < n and js[j + 1] == '{':
                add('tpl', seg, j); j = expr(j + 2); seg = j; continue
            j += 1
        return j
    def expr(i):                          # inside ${ ... } until matching }
        depth = 1; j = i
        while j < n and depth:
            c = js[j]
            if c in '\'"': j = string(j); continue
            if c == '`': j = template(j); continue
            if c == '{': depth += 1
            elif c == '}': depth -= 1
            j += 1
        return j
    def string(i):
        q = js[i]; j = i + 1
        while j < n and js[j] != q:
            if js[j] == '\\': j += 1
            j += 1
        add('str', i + 1, j); return j + 1
    while i < n:
        c = js[i]
        if c in '\'"': i = string(i); prev = 'v'; continue
        if c == '`': i = template(i); prev = 'v'; continue
        if c == '/' and i + 1 < n and js[i + 1] not in '/*' and (prev == '' or prev in '(,=:[!&|?{};'):
            j = i + 1; cls = False
            while j < n:
                if js[j] == '\\': j += 2; continue
                if js[j] == '[': cls = True
                elif js[j] == ']': cls = False
                elif js[j] == '/' and not cls: break
                elif js[j] == '\n': break
                j += 1
            add('re', i + 1, j); i = j + 1; prev = 'v'; continue
        if not c.isspace(): prev = c if c in '(,=:[!&|?{};' else 'v'
        i += 1
    return out
if __name__ == '__main__':
    s = open(sys.argv[1], encoding='utf-8').read()
    res = []
    for m in re.finditer(r'<script[^>]*>(.*?)</script>', s, re.S):
        res += scan(m.group(1), m.start(1))
    # HTML 본문(스크립트 밖)의 한글
    for m in re.finditer(r'>([^<>]*[가-힣][^<>]*)<', re.sub(r'<script[^>]*>.*?</script>', lambda x: ' ' * len(x.group(0)), s, flags=re.S)):
        res.append({'kind': 'html', 'start': m.start(1), 'end': m.end(1), 'text': m.group(1)})
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
    print(len(res), 'pieces,', len({r['text'] for r in res}), 'unique,', sum(len(r['text']) for r in res), 'chars')
