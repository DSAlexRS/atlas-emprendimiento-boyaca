# Publicación en Streamlit Community Cloud

## Preparación

1. Cree un repositorio de GitHub con el contenido de esta carpeta.
2. Confirme que estén incluidos `app.py`, `requirements.txt`, `.streamlit/`,
   `src/` y `data/`.
3. No incluya `.venv/`, archivos temporales ni `secrets.toml`.

## Despliegue

1. Ingrese a <https://share.streamlit.io/>.
2. Conecte su cuenta de GitHub.
3. Seleccione el repositorio y la rama principal.
4. Indique `app.py` como archivo de entrada.
5. En configuración avanzada, utilice Python 3.12.
6. Elija un subdominio disponible y despliegue.

La plataforma instalará las dependencias de `requirements.txt` y asignará una
URL terminada en `streamlit.app`.

## Actualizaciones

Los cambios enviados a la rama conectada se reflejan en la aplicación. Si se
modifican los análisis, reconstruya primero `data/` con
`scripts/build_dashboard_data.py` desde el proyecto de investigación y luego
actualice el repositorio público.

## Datos y privacidad

La aplicación distribuye únicamente estadísticas municipales agregadas. No
requiere credenciales ni almacena respuestas de los visitantes.
