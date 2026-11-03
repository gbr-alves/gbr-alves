"""Gera todos os SVGs de assets/ (banner, buttons, sections).
Uso: python scripts/generate_assets.py
(o registro.svg é sobrescrito depois pelo update_registro.py)"""
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
OUT = ROOT
FONT = "'Courier New', Courier, monospace"
W, G, D, K = "#ffffff", "#8a8a8a", "#222222", "#000000"

def svg(w, h, body, name):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">\n{body}\n</svg>\n'
    sub = "banner" if name.startswith("banner") else "buttons" if name.startswith("btn-") else "sections"
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    open(os.path.join(OUT, sub, name), "w", encoding="utf-8").write(s)

def T(x, y, s, size=14, fill=W, anchor="start", weight="normal", extra=""):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{s}</text>'

def R(x, y, w, h, fill="none", stroke="none", sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def dbox(x, y, w, h, color=W):
    return R(x, y, w, h, K, color, 3) + R(x+7, y+7, w-14, h-14, "none", color, 1)

def section(title, w=900):
    return (f'<polygon points="12,8 18,14 12,20 6,14" fill="{W}"/>' +
            T(26, 19, title, 16, W, extra='letter-spacing="1"') +
            f'<line x1="{26+len(title)*10+14}" y1="10" x2="{w-4}" y2="10" stroke="{W}" stroke-width="1"/>' +
            f'<line x1="{26+len(title)*10+14}" y1="16" x2="{w-4}" y2="16" stroke="{W}" stroke-width="1"/>')

def sprite(rows, px, ox, oy, colors):
    out = []
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c in colors:
                out.append(R(ox+i*px, oy+j*px, px, px, colors[c]))
    return "".join(out)

WIZ = [
 "....WW....",
 "...WWWW...",
 "..WWWWWW..",
 "...WWWW...",
 ".WWWWWWWW.",
 "..WGWWGW..",
 "..WWWWWW..",
 "..WWGGWW..",
 ".WWWWWWWW.",
 ".WGGGGGGW.",
 ".WGGGGGGW.",
 "..GGGGGG..",
 "..WW..WW..",
]
def wizard(px, ox, oy):
    return sprite(WIZ, px, ox, oy, {"W": W, "G": "#9a9a9a"}) + \
        R(ox+10*px+px//2, oy+3*px, px, 10*px, "#777") + R(ox+10*px, oy+2*px, 2*px, px*2, "#aaa")

# ---------- banner ----------
b = R(4, 4, 892, 292, K, W, 4) + R(14, 14, 872, 272, "none", G, 1)
import random
random.seed(7)
for _ in range(14):
    b += R(random.randint(30, 870), random.randint(30, 260), 3, 3, W, extra=f'opacity="{random.choice([0.3,0.6,1])}"')
b += T(450, 56, "PLAYER 1 · LV 1", 15, G, "middle")
b += T(120, 112, "BUFF! INT +10", 12, W, "middle")
b += f'<circle cx="120" cy="190" r="52" fill="none" stroke="{G}" stroke-width="3" opacity="0.8">' \
     f'<animate attributeName="r" values="50;56;50" dur="2.4s" repeatCount="indefinite"/></circle>'
b += f'<g>{wizard(7, 85, 148)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="1.6s" repeatCount="indefinite"/></g>'
b += R(14, 244, 210, 4, "#333")

CYCLE = "10s"
# nome escondido atrás do muro; aparece quando os tijolos quebram
b += (f'<text x="450" y="140" font-size="44" fill="{W}" text-anchor="middle" font-weight="bold" letter-spacing="2" opacity="0">GABRIEL ALVES'
      f'<animate attributeName="opacity" keyTimes="0;0.2;0.3;0.9;0.95;1" values="0;0;1;1;0;0" dur="{CYCLE}" repeatCount="indefinite"/></text>')

# muro de tijolos: 5 fileiras, cada tijolo cai e gira quando a magia acerta
random.seed(11)
bricks = []
for row in range(5):
    y0 = 76 + row*20
    if row % 2 == 0:
        parts = [(250 + k*40, 38) for k in range(10)]
    else:
        parts = [(250, 18)] + [(270 + k*40, 38) for k in range(9)] + [(630, 18)]
    for (x0, w0) in parts:
        bricks.append((x0, y0, w0))
for (x0, y0, w0) in bricks:
    cx, cy = x0 + w0/2, y0 + 9
    dx = random.randint(-70, 70) + (cx-450)*0.25
    dy = random.randint(110, 190)
    ang = random.randint(-120, 120)
    delay = (cx-250)/400*0.04  # leve onda da esquerda p/ direita
    t1, t2 = 0.2+delay, 0.34+delay
    kt = f"0;{t1:.3f};{t2:.3f};0.95;1"
    b += (f'<g>{R(x0, y0, w0, 18, "#555", W, 1)}'
          f'<animateTransform attributeName="transform" type="translate" keyTimes="{kt}" values="0 0;0 0;{dx:.0f} {dy};{dx:.0f} {dy};0 0" dur="{CYCLE}" repeatCount="indefinite"/>'
          f'<animateTransform attributeName="transform" type="rotate" additive="sum" keyTimes="{kt}" values="0 {cx} {cy};0 {cx} {cy};{ang} {cx} {cy};{ang} {cx} {cy};0 {cx} {cy}" dur="{CYCLE}" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" keyTimes="{kt}" values="1;1;0;0;1" dur="{CYCLE}" repeatCount="indefinite"/></g>')

# magia: bola de energia do cajado até o muro + flash no impacto
b += (f'<circle r="7" fill="{W}" cx="162" cy="166" opacity="0">'
      f'<animate attributeName="cx" keyTimes="0;0.12;0.2;1" values="162;162;250;250" dur="{CYCLE}" repeatCount="indefinite"/>'
      f'<animate attributeName="cy" keyTimes="0;0.12;0.2;1" values="166;166;130;130" dur="{CYCLE}" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" keyTimes="0;0.11;0.12;0.2;0.201;1" values="0;0;1;1;0;0" dur="{CYCLE}" repeatCount="indefinite"/></circle>')
b += (f'<circle cx="250" cy="130" r="4" fill="none" stroke="{W}" stroke-width="4" opacity="0">'
      f'<animate attributeName="r" keyTimes="0;0.2;0.34;1" values="4;4;190;190" dur="{CYCLE}" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" keyTimes="0;0.2;0.21;0.34;1" values="0;0;1;0;0" dur="{CYCLE}" repeatCount="indefinite"/></circle>')

b += T(450, 215, "DESENVOLVEDOR FULLSTACK EM FORMAÇÃO", 15, W, "middle")
b += T(250, 250, "EXP", 13, W, "end")
b += R(262, 239, 440, 12, "#111", G, 1) + R(262, 239, 220, 12, W)
b += T(716, 250, "50/100", 13, G)
b += f'<text x="450" y="276" font-size="15" fill="{W}" text-anchor="middle">PRESS START<animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/></text>'
svg(900, 300, b, "banner.svg")

# ---------- buttons ----------
def btn(name, label, icon):
    body = R(2, 2, 186, 40, K, W, 3) + icon + T(110, 30, label, 22, W, "middle", "bold")
    svg(190, 44, body, name)
btn("btn-linkedin.svg", "LINKEDIN", f'<polygon points="22,13 22,31 36,22" fill="{W}"/>')
btn("btn-email.svg", "E-MAIL",
    R(16, 14, 24, 16, "none", W, 2) + f'<polyline points="16,14 28,24 40,14" fill="none" stroke="{W}" stroke-width="2"/>')
btn("btn-sp.svg", "SUA CIDADE",
    f'<circle cx="28" cy="20" r="6" fill="none" stroke="{W}" stroke-width="3"/><polygon points="22,24 34,24 28,35" fill="{W}"/>')

# ---------- sobre mim ----------
b = section("SOBRE MIM") + dbox(6, 30, 888, 130)
b += T(30, 62, "GABRIEL:", 16, W, extra='letter-spacing="1"')
for i, ln in enumerate([
    "Oi! Eu me chamo Gabriel, tenho XX anos e moro em SUA_CIDADE.",
    "Conte aqui o que te trouxe para a programação, sua curiosidade",
    "e o que você estuda hoje (ex.: curso e faculdade)."]):
    b += T(30, 90+i*22, ln, 14, "#cfcfcf")
svg(900, 170, b, "sobre-mim.svg")

# ---------- ficha ----------
b = section("FICHA DO PERSONAGEM") + dbox(6, 30, 888, 190)
def kv(x, y, k, v):
    return T(x, y, k, 12, G, extra='letter-spacing="1"') + T(x, y+20, v, 14, W)
b += kv(30, 62, "CLASSE", "Desenvolvedor FullStack em formação")
b += kv(470, 62, "ESPECIALIDADE", "Sua especialidade · Grimório em construção")
b += kv(30, 114, "GUILDA", "SEU CURSO · SUA FACULDADE")
b += kv(470, 114, "MISSÃO PRINCIPAL", "Estágio em TI")
b += T(30, 184, "NÍVEL 1 · SEMESTRE 1", 13, W) + T(866, 184, "25%", 13, G, "end")
b += R(30, 192, 836, 12, "#111", G, 1) + R(30, 192, 209, 12, W)
svg(900, 230, b, "ficha.svg")

# ---------- mapa ----------
b = section("MAPA DA JORNADA")
xs = [130, 315, 450, 585, 770]
xs = [120, 300, 480, 660, 840]
y = 120
b += f'<line x1="{xs[0]}" y1="{y}" x2="{xs[2]}" y2="{y}" stroke="{W}" stroke-width="4"/>'
b += f'<line x1="{xs[2]}" y1="{y}" x2="{xs[4]}" y2="{y}" stroke="{G}" stroke-width="3" stroke-dasharray="8 8"/>'
labels = ["MONTAR PCS", "CURSOS DE TI", "SEU CURSO", "ESTÁGIO EM TI", "CHEFÃO FULLSTACK"]
for i, x in enumerate(xs):
    if i < 2:
        b += R(x-22, y-22, 44, 44, W) + f'<polyline points="{x-10},{y} {x-3},{y+8} {x+11},{y-8}" fill="none" stroke="{K}" stroke-width="4"/>'
    elif i == 2:
        b += R(x-26, y-26, 52, 52, K, W, 4) + T(x, y+9, "3", 26, W, "middle", "bold")
        b += f'<g>{wizard(3, x-15, y-85)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="1.4s" repeatCount="indefinite"/></g>'
    elif i == 3:
        b += R(x-22, y-22, 44, 44, K, G, 2, 'stroke-dasharray="5 4"') + R(x-9, y-2, 18, 14, G) + f'<path d="M{x-6},{y-2} v-6 a6,6 0 0 1 12,0 v6" fill="none" stroke="{G}" stroke-width="3"/>'
    else:
        b += R(x-22, y-22, 44, 44, K, G, 2, 'stroke-dasharray="5 4"') + f'<polygon points="{x-12},{y+8} {x-12},{y-6} {x-6},{y} {x},{y-8} {x+6},{y} {x+12},{y-6} {x+12},{y+8}" fill="{G}"/>'
    c = W if i <= 2 else G
    w1, w2 = (labels[i].split(" ", 1) + [""])[:2] if i != 4 else ("CHEFÃO", "FULLSTACK")
    b += T(x, y+52, w1, 13, c, "middle") + T(x, y+70, w2, 13, c, "middle")
svg(900, 220, b, "mapa.svg")

# ---------- atributos ----------
b = section("ATRIBUTOS") + dbox(6, 30, 888, 270)
attrs = [("HARDWARE", 4), ("SUPORTE", 4), ("HTML E CSS", 3), ("LÓGICA", 2), ("GIT E GITHUB", 2), ("DADOS", 2)]
for i, (n, lv) in enumerate(attrs):
    yy = 66 + i*40
    b += T(32, yy+14, n, 18, W)
    for s in range(5):
        b += R(300 + s*118, yy, 112, 20, W if s < lv else "#1e1e1e")
svg(900, 310, b, "atributos.svg")

# ---------- conquistas ----------
b = section("CONQUISTAS")
items = [("Primeiro", "commit"), ("Fundamentos", "de TI"), ("Trabalho", "em guilda"), ("Manutenção", "de PCs"), ("Primeiro", "estágio")]
def icon(i, cx, cy):
    if i == 0: return f'<circle cx="{cx}" cy="{cy}" r="7" fill="{W}"/><line x1="{cx}" y1="{cy-18}" x2="{cx}" y2="{cy+18}" stroke="{W}" stroke-width="3"/>'
    if i == 1: return R(cx-12, cy-12, 24, 24, "none", W, 3) + R(cx-5, cy-5, 10, 10, W) + "".join(f'<line x1="{cx+d}" y1="{cy-18}" x2="{cx+d}" y2="{cy-12}" stroke="{W}" stroke-width="2"/><line x1="{cx+d}" y1="{cy+12}" x2="{cx+d}" y2="{cy+18}" stroke="{W}" stroke-width="2"/>' for d in (-6, 0, 6))
    if i == 2: return "".join(f'<circle cx="{cx+d}" cy="{cy-8}" r="4" fill="{W}"/>' + R(cx+d-5, cy-2, 10, 12, W) for d in (-14, 0, 14))
    if i == 3: return f'<line x1="{cx-14}" y1="{cy+14}" x2="{cx+12}" y2="{cy-12}" stroke="{W}" stroke-width="6"/><circle cx="{cx+13}" cy="{cy-13}" r="6" fill="none" stroke="{W}" stroke-width="3"/>'
    return R(cx-11, cy-4, 22, 18, G) + f'<path d="M{cx-7},{cy-4} v-6 a7,7 0 0 1 14,0 v6" fill="none" stroke="{G}" stroke-width="3"/>'
for i, (a, c) in enumerate(items):
    x = 6 + i*180
    if i < 4:
        b += R(x, 30, 168, 130, K, W, 3)
        col = W
    else:
        b += R(x, 30, 168, 130, K, G, 2, 'stroke-dasharray="6 5"'); col = G
    b += icon(i, x+84, 78) + T(x+84, 125, a, 13, col, "middle") + T(x+84, 142, c, 13, col, "middle")
svg(900, 170, b, "conquistas.svg")

# ---------- inventário ----------
b = section("INVENTÁRIO") + dbox(6, 30, 888, 130)
slots = ["HTML", "CSS", "Git", "GitHub", "VS Code", "Chave", "Café", "JS"]
def sicon(i, cx, cy, col):
    if i == 0: return T(cx, cy+8, "</>", 24, col, "middle", "bold")
    if i == 1: return T(cx, cy+8, "{ }", 24, col, "middle", "bold")
    if i == 2: return f'<circle cx="{cx-8}" cy="{cy-10}" r="4" fill="{col}"/><circle cx="{cx-8}" cy="{cy+12}" r="4" fill="{col}"/><circle cx="{cx+10}" cy="{cy-2}" r="4" fill="{col}"/><path d="M{cx-8},{cy-6} V{cy+8} M{cx-8},{cy+2} Q{cx-8},{cy-2} {cx+10},{cy-2}" fill="none" stroke="{col}" stroke-width="3"/>'
    if i == 3: return f'<polygon points="{cx-14},{cy+12} {cx-14},{cy-12} {cx-6},{cy-6} {cx+6},{cy-6} {cx+14},{cy-12} {cx+14},{cy+12} {cx},{cy+16}" fill="{col}"/>'
    if i == 4: return R(cx-14, cy-12, 28, 24, "none", col, 3) + f'<line x1="{cx-14}" y1="{cy-5}" x2="{cx+14}" y2="{cy-5}" stroke="{col}" stroke-width="3"/>' + T(cx, cy+8, "&lt;/&gt;".replace("&lt;", "<").replace("&gt;", ">"), 10, col, "middle")
    if i == 5: return f'<circle cx="{cx-8}" cy="{cy}" r="7" fill="none" stroke="{col}" stroke-width="3"/><line x1="{cx-1}" y1="{cy}" x2="{cx+15}" y2="{cy}" stroke="{col}" stroke-width="3"/><line x1="{cx+9}" y1="{cy}" x2="{cx+9}" y2="{cy+7}" stroke="{col}" stroke-width="3"/>'
    if i == 6: return R(cx-11, cy-6, 20, 18, "none", col, 3) + f'<path d="M{cx+9},{cy-2} h4 v8 h-4" fill="none" stroke="{col}" stroke-width="3"/>' + f'<line x1="{cx-8}" y1="{cy-12}" x2="{cx-8}" y2="{cy-9}" stroke="{col}" stroke-width="2"/><line x1="{cx-1}" y1="{cy-12}" x2="{cx-1}" y2="{cy-9}" stroke="{col}" stroke-width="2"/>'
    return T(cx, cy+10, "?", 30, col, "middle", "bold")
for i, n in enumerate(slots):
    x = 28 + i*108
    col = G if i == 7 else W
    b += R(x, 50, 98, 90, K, col, 3) + sicon(i, x+49, 88, col) + T(x+49, 130, n, 12, col, "middle")
svg(900, 170, b, "inventario.svg")

# ---------- missões ----------
b = section("DIÁRIO DE MISSÕES") + dbox(6, 30, 888, 150)
rows = [("SEU_PROJETO_1 — descrição curta", "EM ANDAMENTO", False), ("SEU_PROJETO_2 — descrição curta", "EM ANDAMENTO", False), ("Criar meu README de perfil", "CONCLUÍDA", True)]
for i, (t, tag, done) in enumerate(rows):
    yy = 72 + i*44
    col = G if done else W
    b += (f'<polyline points="30,{yy-6} 36,{yy} 46,{yy-12}" fill="none" stroke="{G}" stroke-width="3"/>' if done else T(34, yy+2, "!", 20, W, "middle", "bold"))
    b += T(62, yy, t, 15, col, extra='text-decoration="line-through"' if done else "")
    wd = 140
    b += R(740, yy-20, wd, 28, K, col, 2) + T(740+wd/2, yy, tag, 12, col, "middle")
    if i < 2: b += f'<line x1="26" y1="{yy+14}" x2="874" y2="{yy+14}" stroke="{G}" stroke-width="1" stroke-dasharray="4 4"/>'
svg(900, 190, b, "missoes.svg")

# ---------- registro ----------
b = section("REGISTRO DE AVENTURA")
b += dbox(6, 30, 280, 170)
b += T(24, 62, "STATUS", 17, W)
for i, (k, v) in enumerate([("Commits", "0"), ("Pull requests", "0"), ("Issues", "0"), ("Estrelas", "0")]):
    yy = 92 + i*28
    b += T(24, yy, k, 12, G) + T(268, yy, v, 14, W, "end") + f'<line x1="24" y1="{yy+8}" x2="268" y2="{yy+8}" stroke="{G}" stroke-width="1" stroke-dasharray="3 3"/>'
b += dbox(306, 30, 288, 170)
b += T(324, 62, "MAGIAS", 17, W)
b += R(324, 74, 250, 12, "#333") + R(324, 74, 200, 12, W) + R(524, 74, 25, 12, "#bbb") + R(549, 74, 15, 12, "#777")
for i, (k, v, c) in enumerate([("HTML", "80,0%", W), ("Python", "10,3%", "#bbb"), ("CSS", "7,3%", "#777"), ("JavaScript", "2,4%", "#555")]):
    yy = 116 + i*24
    b += R(324, yy-10, 10, 10, c) + T(342, yy, k, 12, W) + T(574, yy, v, 12, G, "end")
b += dbox(606, 30, 288, 170)
b += T(624, 62, "COMBO", 17, W)
b += T(750, 130, "0", 56, W, "middle", "bold") + T(750, 152, "dias seguidos", 12, G, "middle")
b += f'<line x1="624" y1="166" x2="876" y2="166" stroke="{G}" stroke-width="1" stroke-dasharray="3 3"/>'
b += T(624, 188, "Recorde", 12, G) + T(876, 188, "0 DIAS", 14, W, "end")
svg(900, 210, b, "registro.svg")

# ---------- minigame ----------
b = section("MINIGAME") + dbox(6, 30, 888, 150)
random.seed(3)
cols, rows_n, pitch = 52, 7, 16
for c in range(cols):
    for r in range(rows_n):
        v = D
        if c > 44 and random.random() < 0.45: v = random.choice(["#555", "#999", W])
        b += R(30 + c*pitch, 50 + r*pitch, 12, 12, v)
def pac(x, y, delay, ghost=False):
    if ghost:
        return (f'<g><path d="M{x-7},{y+7} v-8 a7,7 0 0 1 14,0 v8 l-3,-3 l-4,3 l-4,-3 z" fill="{W}"/>' + R(x-4, y-3, 3, 3, K) + R(x+1, y-3, 3, 3, K) +
                f'<animateTransform attributeName="transform" type="translate" values="0 0;700 0" dur="9s" begin="{delay}s" repeatCount="indefinite"/></g>')
    return (f'<g><path d="M{x},{y} L{x+8},{y-6} A9,9 0 1 0 {x+8},{y+6} Z" fill="{W}"><animate attributeName="opacity" values="1;1" dur="1s" repeatCount="indefinite"/></path>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;700 0" dur="9s" repeatCount="indefinite"/></g>')
b += pac(60, 82, 0) + pac(30, 66, 0.2, True) + pac(20, 98, 0.4, True)
b += T(30, 170, "SCORE 0", 13, W) + T(866, 170, "1 UP", 13, W, "end")
svg(900, 190, b, "minigame.svg")

# ---------- continue ----------
b = R(0, 0, 900, 140, K) + T(450, 52, "CONTINUE?", 40, W, "middle", "bold")
for i in range(10):
    a, c = i/10, (i+1)/10
    b += (f'<text x="450" y="98" font-size="40" fill="{W}" text-anchor="middle" font-weight="bold" opacity="0">{9-i}'
          f'<animate attributeName="opacity" calcMode="discrete" keyTimes="0;{a};{c};1" values="0;1;0;0" dur="10s" repeatCount="indefinite"/></text>')
b += T(450, 128, "insira uma oportunidade de estágio", 14, G, "middle")
svg(900, 140, b, "continue.svg")

# ---------- rodapé ----------
b = R(0, 0, 900, 110, K) + T(450, 40, "OBRIGADO POR JOGAR", 20, W, "middle")
b += f'<polyline points="400,66 407,73 418,60" fill="none" stroke="{G}" stroke-width="3"/>' + T(428, 72, "JOGO SALVO", 14, G)
b += R(0, 92, 900, 18, "#555") + R(0, 92, 900, 3, "#888")
for x in (60, 270, 480, 690, 860): b += R(x, 100, 18, 3, "#888")
b += f'<g>{wizard(3, 26, 53)}<animateTransform attributeName="transform" type="translate" values="0 0;820 0;0 0" dur="14s" repeatCount="indefinite"/></g>'
svg(900, 110, b, "rodape.svg")
print("assets gerados em", os.path.abspath(OUT))
