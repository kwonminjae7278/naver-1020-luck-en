# 포트폴리오용 바로가기 주소: 주소 끝에 #item #place #music #story #chat #rank #energy #gift
ROUTES = ["home", "friends", "keyring", "fortune", "item", "place", "music", "story", "chat", "rank", "energy", "gift"]
OLD_LIST = 'if (["home", "friends", "keyring", "fortune"].indexOf(h) < 0)'
OLD_BOOT = '  } else if (h === "fortune") start(false);'
NEW_BOOT = '''  } else if (["item", "place", "music"].includes(h)) {   // 행운 아이템·장소·플리 상세
    fortuneSeen = true; start(false);
    setTimeout(() => { busy = false; push(h); }, 60);
  } else if (["story", "chat", "rank"].includes(h)) {    // 친구방: 모먼트(수민) · 행운 공구방 · 운세 순위 비교
    fortuneSeen = true; start(false); setTab("friends", true);
    setTimeout(() => {
      busy = false;
      if (h === "story") openStory("sumin");
      else { openChat(); if (h === "rank") setTimeout(() => { busy = false; document.getElementById("chChip").click(); }, 700); }
    }, 60);
  } else if (h === "energy" || h === "gift") {          // 기운 충전(주파수) · 친구에게 주파수 선물하기
    fortuneSeen = true; start(false); openFreq();
    if (h === "gift") { const t0 = Date.now(), iv = setInterval(() => {
      let c; try { c = freqFrame.contentDocument.querySelectorAll(".who__card")[1]; } catch (e) {}
      if (c) { clearInterval(iv); setTimeout(() => c.click(), 250); } else if (Date.now() - t0 > 15000) clearInterval(iv);
    }, 150); }
  } else if (h === "fortune") start(false);'''

def apply(s):
    assert OLD_LIST in s and OLD_BOOT in s
    s = s.replace(OLD_LIST, 'if (' + str(ROUTES).replace("'", '"') + '.indexOf(h) < 0)', 1)
    return s.replace(OLD_BOOT, NEW_BOOT, 1)
