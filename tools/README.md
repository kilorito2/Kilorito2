# Generadores de imágenes del perfil

Los SVG animados del README (árbol de habilidades, radar y tarjetas de proyectos) salen de estos scripts de Python, sin dependencias externas.

| Script | Genera | Qué se edita |
| --- | --- | --- |
| `gen_stack.py` | `stack-dark.svg`, `stack-light.svg` | La lista `NODES`: cada tecnología con su rama, posición y si ya está aprendida (`learned`). Los grises son las que faltan. |
| `gen_radar.py` | `radar-dark.svg`, `radar-light.svg` | La lista `AXES`: nombre y valor (de 1 a 5) de cada área. |
| `gen_cards.py` | `cards/<id>-dark.svg`, `cards/<id>-light.svg` | La lista `CARDS`: nombre, descripción, tecnologías, fecha de último push y si es destacado. |

`icons.json` tiene los logos (simple-icons, licencia CC0) que usan el árbol y las tarjetas.

## Uso

```powershell
cd tools
python gen_stack.py
python gen_radar.py
python gen_cards.py
```

Las imágenes quedan en `tools/salida/`. Para cambiar la carpeta de salida: `$env:OUT_DIR = "ruta"`.

## Al publicar un cambio

GitHub guarda las imágenes en caché. Copiá los SVG a una carpeta nueva (por ejemplo `assets/v7/`) y actualizá las rutas en el `README.md`; si no, el cambio puede tardar en verse.
