import math
W,H=1400,933
ink="#14181f"; muted="#556070"; acc="#1f4fd1"; deck="#2b3340"; wood="#c9a26b"; woodd="#a8834f"; ball="#e6b818"; bg="#eef1f5"
PX,PY=560,712   # pivot apex
def rig(op=1, dash=False, col=ink):
    sw='stroke-dasharray="10 8"' if dash else ''
    f=lambda c:"none" if dash else c
    return f'''<g opacity="{op}" stroke="{col}" {sw} transform="translate({PX-700} {PY-720})">
  <rect x="330" y="690" width="740" height="30" rx="4" fill="{f(deck)}" stroke-width="3"/>
  <path d="M480 690 L480 674 L920 674 L920 690" fill="none" stroke-width="10" stroke-linecap="round"/>
  <path d="M565 676 L650 640 M835 676 L750 640" fill="none" stroke-width="9" stroke-linecap="round"/>
  <rect x="640" y="540" width="120" height="140" rx="14" fill="{f('#3a4352')}" stroke-width="3"/>
  <circle cx="700" cy="580" r="26" fill="{f('#8a94a3')}" stroke-width="3"/>
  <path d="M676 572 L700 330 L724 572" fill="none" stroke-width="9" stroke-linejoin="round"/>
  <path d="M700 330 L700 282" stroke-width="8"/>
  <ellipse cx="700" cy="272" rx="34" ry="11" fill="{f(ink)}" stroke-width="3"/>
  <path d="M600 300 L800 300 M600 300 Q586 304 588 330 L590 352 M800 300 Q814 304 812 330 L810 352" fill="none" stroke-width="7" stroke-linecap="round"/>
  <path d="M700 300 L700 318" stroke-width="10"/>
  <path d="M726 600 L748 628 L736 650" fill="none" stroke-width="5" stroke-linecap="round"/>
</g>'''
rot=lambda a,b:f'<g transform="rotate({a} {PX} {PY})">{b}</g>'
def arc(r,a1,a2):
    p=lambda a:(PX+r*math.cos(math.radians(a)),PY+r*math.sin(math.radians(a)))
    x1,y1=p(a1);x2,y2=p(a2);return f'M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}'
T=lambda x,y,t,s=24,w=600,c=ink:f'<text x="{x}" y="{y}" font-size="{s}" font-weight="{w}" fill="{c}">{t}</text>'
A=3.5
dl=math.tan(math.radians(A))*300  # drop at ball distance
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">
<defs><marker id="ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{acc}"/></marker></defs>
<rect width="{W}" height="{H}" fill="{bg}"/>
<rect x="0" y="800" width="{W}" height="133" fill="#dde2ea"/>
<rect x="150" y="792" width="820" height="10" rx="3" fill="#7d8796"/>
{rot(A, rig(0.25, True, muted))}
<rect x="190" y="752" width="740" height="40" rx="4" fill="{wood}" stroke="{woodd}" stroke-width="3"/>
<path d="M{PX-26} 752 L{PX} {PY} L{PX+26} 752 z" fill="{acc}"/>
<ellipse cx="{PX-300}" cy="{752-(PY+... if False else 0)}" rx="0" ry="0"/>
<ellipse cx="{PX-300}" cy="{752-(40-dl)/2:.1f}" rx="{24+dl*0.4:.1f}" ry="{(40-dl)/2:.1f}" fill="{ball}" stroke="#b8901a" stroke-width="3"/>
<ellipse cx="{PX+300}" cy="{752-(40+dl)/2:.1f}" rx="22" ry="{min(22,(40+dl)/2):.1f}" fill="{ball}" stroke="#b8901a" stroke-width="3"/>
{rot(-A, rig())}
<path d="{arc(520,-103,-77)}" fill="none" stroke="{acc}" stroke-width="6" marker-start="url(#ah)" marker-end="url(#ah)"/>
{T(PX-150,168,"Rocks side to side",30,700,acc)}
<g stroke="{muted}" stroke-width="2" fill="none">
<path d="M{PX+65} 560 L1010 470"/>
<path d="M{PX+330} 690 L1010 590"/>
<path d="M{PX+322} 722 L1010 680"/>
<path d="M{PX+28} 738 L1010 770"/>
<path d="M915 790 L1010 850"/></g>
{T(1020,478,"Trainer bolted to the deck")}
{T(1020,598,"Top deck")}
{T(1020,688,"Air balls or springs")}{T(1020,716,"push it back to level",20,400,muted)}
{T(1020,778,"Centre pivot")}
{T(1020,858,"Base board on a mat")}
{T(60,80,"How a rocker plate works",36,700)}
{T(60,118,"Rear view. The deck rocks on a centre pivot as you pedal; the dashed outline shows the opposite lean.",21,400,muted)}
</svg>'''
open('rocker.svg','w').write(svg)
