#!/usr/bin/env python3
"""Regenera assets/registro.svg com os números reais do seu GitHub.
Uso (no GitHub Actions): GH_USER=seu-usuario GH_TOKEN=... python scripts/update_registro.py
Teste sem rede:          python scripts/update_registro.py --demo
"""
import datetime, json, os, sys, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "sections", "registro.svg")
FONT = "'Courier New', Courier, monospace"
W, G, K = "#ffffff", "#8a8a8a", "#000000"

QUERY = """
query($login:String!){ user(login:$login){
  pullRequests{ totalCount } issues{ totalCount }
  contributionsCollection{ totalCommitContributions
    contributionCalendar{ weeks{ contributionDays{ date contributionCount } } } }
  repositories(ownerAffiliations:OWNER, isFork:false, first:100){ nodes{
    stargazerCount
    languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } } }
}}"""

def api(url, token, data=None):
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
        "User-Agent": "profile-readme"})
    return json.load(urllib.request.urlopen(req))

def fetch(user, token):
    d = api("https://api.github.com/graphql", token,
            json.dumps({"query": QUERY, "variables": {"login": user}}).encode())["data"]["user"]
    # commits de todos os tempos (públicos); se falhar, usa o último ano
    try:
        commits = api(f"https://api.github.com/search/commits?q=author:{user}&per_page=1", token)["total_count"]
    except Exception:
        commits = d["contributionsCollection"]["totalCommitContributions"]
    days = [x for w in d["contributionsCollection"]["contributionCalendar"]["weeks"] for x in w["contributionDays"]]
    days.sort(key=lambda x: x["date"])
    best = cur = 0
    for x in days:
        cur = cur + 1 if x["contributionCount"] > 0 else 0
        best = max(best, cur)
    today = datetime.date.today().isoformat()
    streak = 0
    for x in reversed(days):
        if x["date"] > today:
            continue
        if x["contributionCount"] > 0:
            streak += 1
        elif x["date"] == today:   # hoje ainda pode não ter commit
            continue
        else:
            break
    langs = {}
    stars = 0
    for r in d["repositories"]["nodes"]:
        stars += r["stargazerCount"]
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return dict(commits=commits, prs=d["pullRequests"]["totalCount"], issues=d["issues"]["totalCount"],
                stars=stars, streak=streak, best=best, langs=langs)

def T(x, y, s, size=14, fill=W, anchor="start", weight="normal"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'
def R(x, y, w, h, fill="none", stroke="none", sw=1):
    return f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def dbox(x, y, w, h):
    return R(x, y, w, h, K, W, 3) + R(x+7, y+7, w-14, h-14, "none", W, 1)

def build(s):
    b = ('<polygon points="12,8 18,14 12,20 6,14" fill="#fff"/>' + T(26, 19, "REGISTRO DE AVENTURA", 16) +
         f'<line x1="250" y1="10" x2="896" y2="10" stroke="{W}"/><line x1="250" y1="16" x2="896" y2="16" stroke="{W}"/>')
    b += dbox(6, 30, 280, 170) + T(24, 62, "STATUS", 17)
    for i, (k, v) in enumerate([("Commits", s["commits"]), ("Pull requests", s["prs"]), ("Issues", s["issues"]), ("Estrelas", s["stars"])]):
        yy = 92 + i*28
        b += T(24, yy, k, 12, G) + T(268, yy, str(v), 14, W, "end") + \
             f'<line x1="24" y1="{yy+8}" x2="268" y2="{yy+8}" stroke="{G}" stroke-dasharray="3 3"/>'
    b += dbox(306, 30, 288, 170) + T(324, 62, "MAGIAS", 17)
    total = sum(s["langs"].values()) or 1
    top = sorted(s["langs"].items(), key=lambda kv: -kv[1])[:4]
    shades = [W, "#bbb", "#777", "#555"]
    b += R(324, 74, 250, 12, "#333")
    x = 324
    for (n, v), c in zip(top, shades):
        w = 250 * v / total
        b += R(x, 74, w, 12, c); x += w
    for i, ((n, v), c) in enumerate(zip(top, shades)):
        yy = 116 + i*24
        pct = f"{100*v/total:.1f}".replace(".", ",") + "%"
        b += R(324, yy-10, 10, 10, c) + T(342, yy, n, 12) + T(574, yy, pct, 12, G, "end")
    b += dbox(606, 30, 288, 170) + T(624, 62, "COMBO", 17)
    b += T(750, 130, str(s["streak"]), 56, W, "middle", "bold") + T(750, 152, "dias seguidos", 12, G, "middle")
    b += f'<line x1="624" y1="166" x2="876" y2="166" stroke="{G}" stroke-dasharray="3 3"/>'
    b += T(624, 188, "Recorde", 12, G) + T(876, 188, f'{s["best"]} DIAS', 14, W, "end")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 210" width="900" height="210" font-family="{FONT}">\n{b}\n</svg>\n')

if __name__ == "__main__":
    if "--demo" in sys.argv:
        stats = dict(commits=68, prs=0, issues=0, stars=0, streak=0, best=5,
                     langs={"HTML": 800, "Python": 103, "CSS": 73, "JavaScript": 24})
    else:
        stats = fetch(os.environ["GH_USER"], os.environ["GH_TOKEN"])
    open(OUT, "w", encoding="utf-8").write(build(stats))
    print("registro.svg atualizado:", stats)
