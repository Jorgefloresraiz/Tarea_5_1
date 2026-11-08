"""CLI de apoyo exploratorio QA. No decide criticidad ni cumplimiento."""
import argparse,json
from pathlib import Path
from modelo import cargar,COLS,ajustar,ROOT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--csv',type=Path,default=ROOT/'datasets/qa_simulado.csv');ap.add_argument('--salida',type=Path,default=Path('salida_qa'));args=ap.parse_args()
    r=json.loads((Path(__file__).parent/'evidencia/validacion.json').read_text())
    train=cargar().iloc[r['desarrollo']];s,m=ajustar(train[COLS].to_numpy(float),r['prueba']['k'])
    nuevos=cargar(args.csv);nuevos['grupo']=m.predict(s.transform(nuevos[COLS].to_numpy(float)))
    args.salida.mkdir(parents=True,exist_ok=True);nuevos.to_csv(args.salida/'asignaciones.csv',index=False)
    perfiles=nuevos.groupby('grupo')[COLS].mean().round(3)
    perfiles.to_csv(args.salida/'perfiles.csv')
    print('DEMOSTRACIÓN CON DATOS SINTÉTICOS. No autoriza decisiones regulatorias ni liberación de lotes.')
    print(perfiles.to_string());print('Acción: QA revisa capacidad y seguimiento de cada grupo; los números de grupo no son niveles de criticidad.')
    print('Resultados:',args.salida.resolve())
if __name__=='__main__': main()
