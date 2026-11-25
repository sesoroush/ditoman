"""Probe IMI-100: fetch the BusinessEngine client scripts so the ranking data call can be reproduced."""
import pathlib, urllib.request
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "probe"
OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
B = "https://imi100.imi.ir/DesktopModules/BusinessEngine/ClientApp/"
for name in ["controllers/module-builder/module.js", "services/services.js", "services/action-manager.js", "module-app.js"]:
    try:
        req = urllib.request.Request(B + name + "?cdv=1501", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=40) as r:
            (OUT / ("js-" + name.split("/")[-1])).write_bytes(r.read())
    except Exception as e:  # noqa
        (OUT / ("js-" + name.split("/")[-1])).write_text("ERROR " + str(e), encoding="utf-8")
print("ok")
