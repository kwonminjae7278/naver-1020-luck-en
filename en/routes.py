# 포트폴리오용 바로가기 주소: 주소 끝에 #item #place #music #story #chat #rank #energy #gift
ROUTES = ["home", "friends", "keyring", "fortune", "item", "place", "music", "story", "chat", "rank", "energy", "gift", "rub"]
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
  } else if (h === "rub") {                              // 주파수 선물: 수민에게 보낸 카드를 문지르는 화면으로 바로
    fortuneSeen = true; start(false); openFreq();
    freqFrame.style.transition = "opacity .25s"; freqFrame.style.opacity = "0";
    const W = ms => new Promise(r => setTimeout(r, ms)), show = v => freqFrame.style.opacity = v ? "1" : "0";
    (async () => {
      let d, w;
      for (let i = 0; i < 100; i++) { try { d = freqFrame.contentDocument; w = freqFrame.contentWindow; if (d.querySelectorAll(".who__card")[1]) break; } catch (e) {} await W(150); }
      const btn = t => [...d.querySelectorAll("button")].find(b => b.innerText.trim() === t);
      const until = async (f, n = 60) => { for (let i = 0; i < n; i++) { const v = f(); if (v) return v; await W(150); } };
      const setv = (el, v) => { Object.getOwnPropertyDescriptor(w.HTMLTextAreaElement.prototype, "value").set.call(el, v); el.dispatchEvent(new w.Event("input", { bubbles: true })); };
      try {
        d.querySelectorAll(".who__card")[1].click();
        (await until(() => [...d.querySelectorAll(".friend-row")].find(b => /sumin/i.test(b.innerText)))).click(); await W(150);
        btn("Next").click();
        (await until(() => d.querySelector(".compose__card"))).click();
        const ta = await until(() => d.querySelector("textarea.compose__input"));
        setv(ta, "She wants to get back with her ex… she needs calming energy");
        ta.dispatchEvent(new w.FocusEvent("focusout", { bubbles: true }));
        (await until(() => btn("Calm Down"))).click(); await W(150);
        btn("Next").click();
        (await until(() => btn("Create Frequency"))).click();
        show(true);                                      // 생성 중 화면은 그대로 보여 줌
        await until(() => d.querySelector(".signal__dots"), 120); show(false);
        d.querySelectorAll(".signal__dots button")[1].click(); await W(700);
        btn("Select").click();
        setv(await until(() => d.querySelector("textarea.gift__message")), "play this and just sleep!!!!!!!!"); await W(150);
        btn("Send Energy").click(); await W(400);
      } catch (e) {}
      show(true);
    })();
  } else if (h === "fortune") start(false);'''

def apply(s):
    assert OLD_LIST in s and OLD_BOOT in s
    s = s.replace(OLD_LIST, 'if (' + str(ROUTES).replace("'", '"') + '.indexOf(h) < 0)', 1)
    return s.replace(OLD_BOOT, NEW_BOOT, 1)
