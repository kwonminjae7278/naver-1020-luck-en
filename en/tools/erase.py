# 이미지 속 한글 글자만 지우기: OCR로 찾은 글자 줄(또는 지정한 상자) 안을 주변 색으로 자연스럽게 메움
# (make_assets_v7.py와 같은 방식: 가로·세로 보간으로 시작해 조화 평균으로 수렴 → 단색·그라디언트 배경에서 흔적 없음)
import subprocess, os, re, sys
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
HANG = re.compile(r'[가-힣ㄱ-ㅣ]')

def ocr(path):
    out = subprocess.run([f'{HERE}/ocrbox', path], capture_output=True, text=True).stdout
    res = []
    for l in out.strip().split('\n'):
        if not l: continue
        p, x0, y0, x1, y1, t = l.split('\t', 5)
        res.append((int(x0), int(y0), int(x1), int(y1), t))
    return res

def harmonic_fill(img, mask, iters=1500):
    def interp(a, m):
        out = a.copy(); idx = np.arange(a.shape[1])
        for y in np.nonzero(m.any(1))[0]:
            ok = ~m[y]
            if ok.sum() < 2: continue
            for c in range(a.shape[2]): out[y, m[y], c] = np.interp(idx[m[y]], idx[ok], a[y, ok, c])
        return out
    out = (interp(img, mask) + interp(img.transpose(1, 0, 2), mask.T).transpose(1, 0, 2)) / 2
    for _ in range(iters):
        avg = (np.roll(out, 1, 0) + np.roll(out, -1, 0) + np.roll(out, 1, 1) + np.roll(out, -1, 1)) / 4
        out[mask] = avg[mask]
    return out

CACHE = os.path.join(os.path.dirname(HERE), '.cache')

def erase(path, out, boxes=None, pad=3, hangul_only=True, extra=(), skip=()):
    if boxes is None:
        boxes = [(x0, y0, x1, y1) for x0, y0, x1, y1, t in ocr(path) if (HANG.search(t) or not hangul_only) and not any(s in t for s in skip)]
    boxes = [tuple(int(v) for v in b) for b in list(boxes) + list(extra)]
    # 같은 입력(파일 내용·상자·여백)이면 이전 결과를 그대로 씀 (조화 메움이 느려서)
    import hashlib, shutil
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(open(path, 'rb').read() + repr((boxes, pad)).encode()).hexdigest()[:16]
    cp = os.path.join(CACHE, key + os.path.splitext(out)[1])
    if os.path.exists(cp):
        shutil.copyfile(cp, out); return boxes
    _erase(path, out, boxes, pad)
    shutil.copyfile(out, cp)
    return boxes

def _erase(path, out, boxes, pad):
    im = Image.open(path); mode = im.mode
    a = np.asarray(im.convert('RGBA')).astype(float)
    H, W = a.shape[:2]
    mask = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in boxes:
        mask[max(0, y0 - pad):min(H, y1 + pad), max(0, x0 - pad):min(W, x1 + pad)] = True
    # 알파가 있는 레이어: 색은 미리곱한 값으로 메우고, 투명한 곳은 투명하게 둠
    pm = a.copy(); pm[..., :3] *= pm[..., 3:4] / 255
    filled = harmonic_fill(pm, mask)
    al = np.clip(filled[..., 3:4], 0, 255)
    rgb = np.where(al > 0.5, filled[..., :3] / np.maximum(al, 1e-6) * 255, 0)
    res = np.dstack([np.clip(rgb, 0, 255), al])
    res[~mask] = a[~mask]
    img = Image.fromarray(res.round().astype(np.uint8), 'RGBA')
    if mode != 'RGBA' and not path.endswith('.png'): img = img.convert('RGB')
    if out.endswith('.jpg'): img.convert('RGB').save(out, quality=96, subsampling=0)
    else: img.save(out)
    return boxes

if __name__ == '__main__':
    for p in sys.argv[1:]: print(p, erase(p, p))
