# Beta — Capa visual JARVIS v1.0

## Objetivo
Agregar una segunda apariencia a Beta sin modificar su núcleo estable `beta.py`.

## Apariencias
- Predeterminada: Orbe JARVIS transparente.
- Secundaria: esfera clásica original de Beta.

## Integración
- `beta_inicio_visual.py` importa el `beta.py` existente y conserva una única instancia de `BetaApp`.
- En modo JARVIS oculta únicamente la ventana clásica; el cerebro, voz, memoria, Atlas, Aula y demás módulos siguen vivos.
- En modo clásico cierra el proceso visual JARVIS y vuelve a mostrar la ventana Tk original.
- El selector se añade al menú clásico en tiempo de ejecución; el archivo `beta.py` no se edita.

## Sincronización
El orbe integrado recibe por UDP local (`127.0.0.1`) el estado real de Beta:
- hablando;
- procesando;
- escuchando;
- nivel de boca;
- expresión.

No abre `sounddevice` ni un segundo micrófono.

## Seguridad / fallback
- El paquete no contiene `beta.py`, por lo que no puede sobrescribir el núcleo por accidente.
- Si faltan PySide6/pygame/numpy, el lanzador usa automáticamente la esfera clásica.
- Si el proceso del orbe se cae, el lanzador vuelve a mostrar la esfera clásica.
- Si se cierra Beta, el orbe también termina.

## Dependencias nuevas
- PySide6
- pygame
- numpy

No se requiere sounddevice para la versión integrada.
