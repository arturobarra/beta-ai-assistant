# Beta — Apariencia Orbe JARVIS (integración aditiva)

## Principio de seguridad

Esta integración **no modifica `beta.py`**. El cerebro estable de Beta continúa siendo exactamente el mismo archivo.

Archivos nuevos:

- `beta_inicio_visual.py`: lanzador/capa de apariencia.
- `beta_orbe_integrado.py`: ventana transparente sincronizada con Beta.
- `orbe_jarvis.py`: motor visual proporcionado por el usuario, sin necesidad de integrarlo dentro del núcleo.
- `beta_apariencia.json`: preferencia visual; JARVIS es predeterminado.
- `INSTALAR_APARIENCIA_BETA.bat`: instala PySide6, pygame y numpy.
- `INICIAR_BETA_ORBE.bat`: inicia Beta usando la capa visual.

`orbe_transparente.py` puede conservarse como demostración independiente; la integración usa una adaptación separada para no abrir un segundo micrófono.

## Instalación

1. Copiar todos los archivos del paquete dentro de `A:\Beta`, junto a `beta.py`.
2. Ejecutar una sola vez `INSTALAR_APARIENCIA_BETA.bat`.
3. Iniciar Beta con `INICIAR_BETA_ORBE.bat`.

También puede ejecutarse:

```powershell
& "C:\Users\MJRABE\AppData\Local\Programs\Python\Python312\python.exe" "A:\Beta\beta_inicio_visual.py"
```

## Apariencias

Predeterminada:

- **Orbe JARVIS transparente**.

Secundaria:

- **Esfera clásica** de Beta, sin modificarla.

En el Orbe JARVIS: clic derecho → `Apariencia de Beta` → `Esfera clásica`.

En la esfera clásica: clic derecho → `Apariencia` → `Orbe JARVIS (predeterminado)`.

La elección se guarda en `beta_apariencia.json` para el próximo inicio.

## Sin segundo micrófono

Aunque los archivos originales permiten que el orbe abra el micrófono por su cuenta, la versión integrada **no lo hace**. Recibe por UDP local el estado real de Beta: hablando, procesando, escuchando y nivel de boca. Esto evita competir con Vosk/Whisper por el dispositivo de audio.

## Qué se conserva

Todo el núcleo continúa en `beta.py`: voz Daniela, Vosk/Whisper, biometría, Ollama, memoria, recordatorios, Spotify, Control Atlas, IPP, Aula, Constructor, Word, mirada clásica, etc.

Si el orbe no puede iniciar por una dependencia faltante, el lanzador vuelve automáticamente a la esfera clásica.

## Volver al comportamiento anterior

Ejecutar simplemente:

```powershell
& "C:\Users\MJRABE\AppData\Local\Programs\Python\Python312\python.exe" "A:\Beta\beta.py"
```

Eso ignora completamente la capa JARVIS y ejecuta Beta como antes.
