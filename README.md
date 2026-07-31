# Atlas del tejido emprendedor de Boyacá

Micrositio interactivo construido con Streamlit para explorar los perfiles
municipales del tejido emprendedor urbano visible, su estructura productiva,
accesibilidad y organización espacial.

La aplicación desplegada es autocontenida: `app.py` utiliza únicamente los
archivos incluidos en `data/`. Puede ejecutarse dentro del proyecto de
investigación o publicarse como un repositorio independiente. El script de
reconstrucción es una herramienta de mantenimiento y se ejecuta desde el
proyecto analítico completo.

## Abrir localmente

En Windows, haga doble clic en:

`iniciar_dashboard.bat`

El archivo verifica las dependencias, inicia la aplicación y abre
`http://localhost:8501`. La primera ejecución puede tardar mientras instala los
componentes requeridos. Para detener el servidor, presione `Ctrl+C` en la
ventana de comandos.

También puede iniciarse manualmente:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Contenido

- **Panorama territorial:** mapa de perfiles, indicadores generales y
  distribución municipal. Los perfiles y tramos de distancia pueden filtrarse
  desde la barra lateral; los municipios excluidos permanecen en gris.
- **Perfiles municipales:** centroides, indicadores observables, municipios y
  orientaciones de política.
- **Accesibilidad territorial:** gradientes de distancia, candidatos a
  centralidades secundarias y dependencia espacial.
- **Ficha municipal:** comparación de cada municipio con el promedio de su
  perfil y Boyacá; cuatro bloques de gestión, escala, financiación, inclusión,
  localización y tributos; estructura productiva y universos estadísticos.
- **Método y alcance:** fuentes, dimensiones, límites interpretativos y descarga
  de la base pública.

Los mapas permiten desplazamiento, zoom y consulta municipal al pasar el
cursor. La navegación y las tarjetas se adaptan a pantallas compactas; en
móviles la barra lateral inicia cerrada.

## Estructura

```text
dashboard_streamlit/
├── app.py
├── iniciar_dashboard.bat
├── requirements.txt
├── .streamlit/config.toml
├── data/
├── scripts/build_dashboard_data.py
└── src/
```

## Actualizar los datos

Desde la raíz del proyecto de investigación:

```powershell
.\.venv\Scripts\python.exe dashboard_streamlit\scripts\build_dashboard_data.py
```

Primero deben estar ejecutados los notebooks, incluido
`04_auditoria_ampliacion_variables.ipynb`, y debe existir el producto municipal
final:

```powershell
.\.venv\Scripts\python.exe scripts\build_processed_municipal_dataset.py
```

La rutina del tablero selecciona las columnas públicas desde
`data/processed/base_municipal_emprendimiento_boyaca.csv`, copia los resúmenes
espaciales necesarios y simplifica la geometría para publicación.

Después de reconstruir los datos, reinicie el tablero para vaciar la caché
cartográfica.

## Publicación

Streamlit Community Cloud permite publicar aplicaciones gratuitamente en un
subdominio `streamlit.app`. Requiere que el código esté en GitHub. Al crear la
aplicación se selecciona el repositorio, la rama y `app.py` como archivo
principal.

Documentación oficial:

- <https://docs.streamlit.io/deploy/streamlit-community-cloud>
- <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization>
- <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies>

No se requieren secretos, base de datos externa ni servicios pagos para esta
versión.

## Alcance científico

La unidad de análisis es el municipio. Los perfiles son descriptivos y no
constituyen tasas oficiales de informalidad, medidas de supervivencia ni
estimaciones causales del efecto de la distancia.
