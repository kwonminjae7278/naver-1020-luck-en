# 영문판 폰트: ZEN SERIF만 이 페이지에 쓰인 글자 + 기본 라틴 문자로 작게 (Pretendard 대신 시스템 SF Pro 사용)
# 사용: python3 en/make_fonts_en.py [ZEN SERIF 파일]
import re, sys, os
from fontTools import subset
d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
zen = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/Library/Fonts/ZEN-SERIF-TTF-Regular.ttf')
src = open(f'{d}/src.html', encoding='utf-8').read()
text = re.sub(r'data:[^"\')]+', '', src)
chars = set(text) | set(chr(c) for c in range(0x20, 0x7f)) | set('’‘“”—–·…×')
chars = ''.join(sorted(c for c in chars if c >= ' ' and not ('가' <= c <= '힣')))
opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']; opts.name_IDs = ['*']
f = subset.load_font(zen, opts); s = subset.Subsetter(opts); s.populate(text=chars); s.subset(f)
subset.save_font(f, f'{d}/fonts/zen-serif.woff2', opts)
print('zen-serif', os.path.getsize(f'{d}/fonts/zen-serif.woff2') // 1024, 'KB')
