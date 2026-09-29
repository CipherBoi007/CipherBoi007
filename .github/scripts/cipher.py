import random, html
E=html.escape
MONO="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
THEMES={
 "dark": dict(bg="#161b22",grid="#1f2630",border="#30363d",txt="#e6edf3",mut="#a5d6ff",faint="#6e7681",scr1="#8b949e",scr2="#484f58",line="#ffa657"),
 "light":dict(bg="#f6f8fa",grid="#eaeef2",border="#d0d7de",txt="#1f2328",mut="#0a3069",faint="#8c959f",scr1="#57606a",scr2="#afb8c1",line="#953800"),
}
GL="!<>-_/[]{}=+*^?#%&$@0123456789ABCDEFXYZ"

def build(theme):
    c=THEMES[theme]; random.seed(11)
    W,H=1200,400
    def decrypt(x,y,text,size,start,per=.07,steps=10,stagger=.12,color=None,weight=700,glitch=()):
        color=color or c["txt"]; out=[]; cw=size*.6
        for i,ch in enumerate(text):
            cx=x+i*cw
            if ch==" ": continue
            lock=start+i*stagger+steps*per
            for s in range(steps):
                g=random.choice(GL); t=start+i*stagger+s*per
                out.append(f'<text x="{cx:.1f}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{c["scr2"] if s%2 else c["scr1"]}" opacity="0">{E(g)}<set attributeName="opacity" to="1" begin="{t:.2f}s"/><set attributeName="opacity" to="0" begin="{t+per:.2f}s"/></text>')
            if i in glitch:
                off=lock+3+list(glitch).index(i)*2.3; g1=random.choice(GL)
                out.append(f'<text x="{cx:.1f}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" opacity="0"><set attributeName="opacity" to="1" begin="{lock:.2f}s"/><animate attributeName="opacity" values="1;0;0;1;1" keyTimes="0;.001;.03;.031;1" calcMode="discrete" dur="9s" begin="{off:.2f}s" repeatCount="indefinite"/>{E(ch)}</text>')
                out.append(f'<text x="{cx:.1f}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{c["scr1"]}" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.001;.03;1" calcMode="discrete" dur="9s" begin="{off:.2f}s" repeatCount="indefinite"/>{E(g1)}</text>')
            else:
                out.append(f'<text x="{cx:.1f}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" opacity="0"><set attributeName="opacity" to="1" begin="{lock:.2f}s"/>{E(ch)}</text>')
        return "\n".join(out), start+len(text)*stagger+steps*per

    b=[f'<rect width="{W}" height="{H}" rx="15" fill="{c["bg"]}"/>',
       f'<rect width="{W}" height="{H}" rx="15" fill="url(#grid)"/>']
    name="Yogesh V"; size=120; cw=size*.6; nx=(W-len(name)*cw)/2
    hexs=" ".join(f"{ord(ch):02X}" for ch in name)
    b.append(f'<text x="{W/2}" y="92" text-anchor="middle" font-size="15" letter-spacing="3" fill="{c["faint"]}">0x {hexs}</text>')
    s,end=decrypt(nx,228,name,size,.4,glitch=(1,5)); b.append(s)
    b.append(f'<path d="M{nx} 262H{nx}" stroke="{c["line"]}" stroke-width="2"><animate attributeName="d" from="M{nx} 262H{nx}" to="M{nx} 262H{nx+len(name)*cw-cw*.4:.0f}" begin="{end:.2f}s" dur=".9s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></path>')
    line="full stack developer · ai/ml · ramanathapuram, tamil nadu"; ls=16; lx=(W-len(line)*ls*.6)/2
    s2,end2=decrypt(lx,306,line,ls,end+.2,per=.035,steps=5,stagger=.018,color=c["mut"],weight=400); b.append(s2)
    b.append(f'<text x="44" y="{H-36}" font-size="12" letter-spacing="2" fill="{c["faint"]}">CIPHERBOI007</text>')
    b.append(f'<text x="{W-44}" y="{H-36}" text-anchor="end" font-size="12" letter-spacing="2" fill="{c["faint"]}">decrypting…<set attributeName="opacity" to="0" begin="{end2:.2f}s"/></text>')
    b.append(f'<text x="{W-44}" y="{H-36}" text-anchor="end" font-size="12" letter-spacing="2" fill="{c["line"]}" opacity="0">decrypted ✓<set attributeName="opacity" to="1" begin="{end2:.2f}s"/></text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" role="img">
<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern></defs>
{chr(10).join(b)}
</svg>'''

import sys
out=sys.argv[1] if len(sys.argv)>1 else "."
for t in THEMES:
    open(f"{out}/hero_{t}.svg","w").write(build(t))
print("ok")
