"""Builds dark_mode.svg and light_mode.svg: ASCII portrait + neofetch-style info.
Runs locally or in GitHub Actions (set GH_TOKEN to fetch live stats)."""
import os, json, urllib.request, html
from pathlib import Path

USER = "CipherBoi007"
ROOT = Path(__file__).resolve().parents[2]
ART = (ROOT / ".github" / "scripts" / "art.txt").read_text().splitlines()
W = 60  # width of the info column in characters

def stats():
    token = os.environ.get("GH_TOKEN")
    if not token:
        return None
    q = """query($u:String!){ user(login:$u){
      followers{totalCount}
      repositories(ownerAffiliations:OWNER, first:100){ totalCount nodes{ stargazerCount } }
      repositoriesContributedTo(first:1, contributionTypes:[COMMIT,PULL_REQUEST,REPOSITORY,ISSUE]){ totalCount }
      contributionsCollection{ contributionCalendar{ totalContributions } } } }"""
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"u": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    try:
        u = json.load(urllib.request.urlopen(req, timeout=30))["data"]["user"]
    except Exception as e:
        print("stats fetch failed:", e); return None
    return {
        "repos": u["repositories"]["totalCount"],
        "contrib_to": u["repositoriesContributedTo"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
        "contributions": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
    }

def fmt(n):
    return "—" if n is None else f"{n:,}"

def build(theme, s):
    c = {"dark":  dict(bg="#161b22", txt="#c9d1d9", key="#ffa657", val="#a5d6ff", dot="#616e7f", add="#3fb950"),
         "light": dict(bg="#f6f8fa", txt="#24292f", key="#953800", val="#0a3069", dot="#c2cfde", add="#1a7f37")}[theme]
    E = html.escape
    info = []  # each entry: list of (text, colour) segments

    def header(t):
        info.append([(t + " ", c["txt"]), ("—" * (W - len(t) - 1), c["txt"])])
    def section(t):
        info.append([("- " + t + " ", c["txt"]), ("—" * (W - len(t) - 3), c["txt"])])
    def kv(k, v):
        dots = W - len(k) - len(v) - 5
        info.append([(". ", c["dot"]), (k, c["key"]), (": ", c["txt"]), ("." * dots + " ", c["dot"]), (v, c["val"])])
    def blank():
        info.append([(".", c["dot"])])
    def pair(k1, v1, k2, v2):
        half = (W - 3) // 2
        d1 = half - len(k1) - len(v1) - 5
        d2 = W - half - 3 - len(k2) - len(v2) - 3
        info.append([(". ", c["dot"]), (k1, c["key"]), (": ", c["txt"]), ("." * d1 + " ", c["dot"]), (v1, c["val"]),
                     (" | ", c["txt"]), (k2, c["key"]), (": ", c["txt"]), ("." * d2 + " ", c["dot"]), (v2, c["val"])])

    s = s or {}
    header("yogesh@cipherboi007")
    kv("OS", "B.E. CSE, Syed Ammal Engineering College")
    kv("Host", "Zeshin (COO)")
    kv("Kernel", "Full Stack Developer · AI/ML")
    kv("Shell", "Ramanathapuram, Tamil Nadu")
    blank()
    kv("Languages.Programming", "Python, JavaScript, Java, SQL")
    kv("Languages.Web", "Next.js, React.js, HTML, CSS")
    kv("Languages.Real", "English, Tamil")
    blank()
    kv("Stack.Backend", "Spring Boot, Django, FastAPI")
    kv("Stack.Data", "PostgreSQL, AWS, Docker")
    kv("Stack.AI", "CNN, ResNet, EfficientNet, Grad-CAM")
    blank()
    section("Contact")
    kv("Email.Personal", "cipherboi007@gmail.com")
    kv("LinkedIn", "yogesh-v-dev")
    kv("Portfolio", "yogesh-v-dev-ten.vercel.app")
    blank()
    section("GitHub Stats")
    pair("Repos", fmt(s.get("repos")), "Stars", fmt(s.get("stars")))
    pair("Contributions (1y)", fmt(s.get("contributions")), "Followers", fmt(s.get("followers")))

    LH, FS, CW = 20, 16, 9.6
    art_w = max(len(l) for l in ART)
    rows = max(len(ART), len(info))
    ix = 30 + (art_w + 3) * CW
    width = int(ix + W * CW + 30)
    height = rows * LH + 50
    a_off = (rows - len(ART)) // 2
    i_off = (rows - len(info)) // 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,\'Courier New\',monospace" width="{width}px" height="{height}px" font-size="{FS}px">',
           '<style>.a{white-space:pre}</style>',
           f'<rect width="{width}px" height="{height}px" fill="{c["bg"]}" rx="15"/>',
           f'<text x="30" y="30" fill="{c["txt"]}" class="a" xml:space="preserve">']
    for i, l in enumerate(ART):
        out.append(f'<tspan x="30" y="{30 + (i + a_off) * LH}">{E(l)}</tspan>')
    out.append('</text>')
    out.append(f'<text x="{ix:.0f}" y="30" class="a" xml:space="preserve">')
    for i, segs in enumerate(info):
        y = 30 + (i + i_off) * LH
        out.append(f'<tspan x="{ix:.0f}" y="{y}">' + "".join(f'<tspan fill="{col}">{E(t)}</tspan>' for t, col in segs) + '</tspan>')
    out.append('</text></svg>')
    return "\n".join(out)

if __name__ == "__main__":
    s = stats()
    for theme in ("dark", "light"):
        (ROOT / f"{theme}_mode.svg").write_text(build(theme, s), encoding="utf-8")
    print("built", s)
