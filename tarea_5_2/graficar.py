"""Gráficas SVG reproducibles, sin dependencias de visualización."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'tarea_5_2/resultados/analisis.json').read_text())
out=ROOT/'tarea_5_2/graficas';out.mkdir(exist_ok=True)
def svg(): return ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620"><rect width="1200" height="620" fill="white"/><g font-family="Arial,sans-serif" fill="#222">']
def text(s,x,y,t,size=20): s.append(f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(str(t))}</text>')
def axes(s,left,right,top,bottom,xmin,xmax,ymin,ymax,xlabel,ylabel):
 def px(x):return left+(x-xmin)/(xmax-xmin)*(right-left)
 def py(y):return bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
 for i in range(6):
  y=ymin+(ymax-ymin)*i/5;yy=py(y)
  s.append(f'<path d="M {left} {yy} H {right}" stroke="#ddd"/>');text(s,left-65,yy+7,f'{y:.2f}',16)
 for i in range(7):
  x=xmin+(xmax-xmin)*i/6;text(s,px(x)-12,bottom+26,f'{x:.1f}',16)
 s.append(f'<path d="M {left} {top} V {bottom} H {right}" fill="none" stroke="#333"/>')
 text(s,(left+right)/2-45,bottom+60,xlabel);text(s,left,top-20,ylabel)
 return px,py
s=svg();text(s,70,35,'Selección de k en 300 casos simulados de QA',26)
for left,right,key,lo,hi,label in [(85,550,'inercia',600,1400,'Inercia'),(705,1170,'silueta',0,.4,'Silueta media')]:
 px,py=axes(s,left,right,110,500,2,8,lo,hi,'Número de grupos k',label)
 pts=[(px(r['k']),py(r[key])) for r in a['comparacion']]
 s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#205b8f" stroke-width="3"/>')
 for j,(x,y) in enumerate(pts):
  s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="'+('#b24d16' if j==0 else '#205b8f')+'"/>')
text(s,710,65,'Máxima silueta: k = 2 (0.356)',19)
s.append('</g></svg>');(out/'seleccion_k.svg').write_text('\n'.join(s))
s=svg();text(s,80,35,'Segmentación de QA en dos componentes principales',26)
xy=a['pca']['proyeccion'];xs=[v[0] for v in xy];ys=[v[1] for v in xy];v=a['pca']['varianza_explicada_por_componente']
px,py=axes(s,90,1160,105,490,min(xs)-.3,max(xs)+.3,min(ys)-.3,max(ys)+.3,f'PC1 ({v[0]*100:.2f} %)',f'PC2 ({v[1]*100:.2f} %)')
for (x,y),g in zip(xy,a['mejor']['etiquetas']):
 s.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="5" fill="'+('#b24d16' if g==0 else '#205b8f')+'" fill-opacity="0.65"/>')
text(s,90,590,'Naranja: mayor carga (47)   Azul: menor carga (253)   Varianza conservada: 64.39 %',21)
s.append('</g></svg>');(out/'pca_grupos.svg').write_text('\n'.join(s))
print('Gráficas SVG creadas')
