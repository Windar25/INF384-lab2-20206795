# despachos

Modulo de consolidacion de despachos. Calcula tarifas de envio, valida datos de
entrada y administra el ciclo de vida de un pedido.

## Estructura

```
src/despachos/          Codigo fuente
  pedidos.py            Modelo de pedido y transiciones de estado
  tarifas.py            Calculo de tarifas de despacho
  validaciones.py       Validaciones de formato de entrada
tests/                  Pruebas unitarias
docs/                   Documentacion y entregables
.github/workflows/      Definicion del pipeline
```

## Ejecutar en local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest --cov=src --cov-report=term
```

## Pipeline

El pipeline esta definido en `.github/workflows/pipeline.yml` y tiene dos
trabajos:

- `validar`: instala dependencias, ejecuta las pruebas con reporte de cobertura
  y envia el resultado al servicio de analisis de calidad.
- `publicar`: construye el paquete distribuible y lo publica como artefacto de
  la ejecucion.

Se puede ejecutar manualmente desde la pestana **Actions**, con **Run workflow**.

## Configuracion requerida

| Elemento | Donde se configura |
|---|---|
| `SONAR_TOKEN` | Settings -> Secrets and variables -> Actions -> **Secrets** |
| `SONAR_ORG` | Settings -> Secrets and variables -> Actions -> **Variables** |
| `SONAR_PROJECT_KEY` | Settings -> Secrets and variables -> Actions -> **Variables** |

El proyecto en SonarQube Cloud se crea **importando el repositorio** desde
GitHub, no manualmente: asi queda publico, vinculado al repositorio y con
`main` como rama principal. La project key que SonarQube Cloud genera se copia
tal cual en la variable `SONAR_PROJECT_KEY`.

No hay que editar ningun archivo del repositorio para configurar el analisis.

## Version

La version vigente esta en `VERSION` y en `pyproject.toml`.
