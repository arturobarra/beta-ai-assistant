# Beta - Asistente Virtual Local con Inteligencia Artificial

Beta es un asistente virtual desarrollado en Python como proyecto personal de aprendizaje y desarrollo.

El objetivo del proyecto es construir un asistente local capaz de interactuar mediante voz, utilizar inteligencia artificial, mantener memoria persistente, consultar documentación mediante RAG y ejecutar funciones controladas en Windows.

## Versión estable actual

**Beta v3.7.1**

## Características principales

- Reconocimiento rápido de comandos mediante Vosk
- Dictado preciso mediante Faster-Whisper
- Comandos directos protegidos para Agenda, Word y aplicaciones compatibles
- Síntesis de voz local mediante Piper / Daniela
- Inteligencia artificial local con Ollama y Qwen
- Reconocimiento biométrico de hablante
- Modo estricto con wake word y voz autorizada
- Memoria persistente mediante SQLite
- Biblioteca académica y técnica mediante RAG
- Búsqueda semántica con Sentence Transformers
- Enrutamiento inteligente de fuentes
- Integración con Spotify
- Control de aplicaciones mediante Control Atlas
- Agenda Beta integrada con Google Calendar
- Confirmación por voz antes de crear eventos
- Recordatorios por correo configurables
- Apariencia clásica y Orbe/JARVIS
- Sistema de respaldos
- Procesamiento principalmente local

## Arquitectura general

Usuario  
↓  
Vosk  
↓  
Faster-Whisper cuando la orden requiere dictado preciso  
↓  
Reconocimiento de hablante  
↓  
Router / Orquestador  
↓  
Control Atlas / Agenda / Biblioteca / Qwen  
↓  
Piper / Daniela

## Agenda Beta

Beta puede abrir la Agenda mediante voz y crear eventos usando lenguaje natural.

Las operaciones de escritura utilizan Faster-Whisper y requieren confirmación antes de ser enviadas a Google Calendar.

Ejemplo:

`Beta, agenda Kinesiología Benjamín para el 21 de octubre a las 4 de la tarde.`

## Apariencias

Beta dispone de dos formas de inicio:

- `INICIAR_BETA.bat` — inicio estándar.
- `INICIAR_BETA_ORBE.bat` — apariencia Orbe/JARVIS.

Ambas utilizan el mismo núcleo estable `beta.py`.

## Privacidad

Las bases de datos personales, documentos, modelos de IA, credenciales, tokens y archivos privados no forman parte de este repositorio.

## Tecnologías

Python, SQLite, Vosk, Faster-Whisper, Piper, Ollama, Qwen, Sentence Transformers, SpeechBrain, PyMuPDF, Tkinter, Pygame, Spotify Web API y Google Calendar.

## Autor

**Jonathan Gonzalez Barra**

Proyecto desarrollado como parte de mi aprendizaje y formación en Ingeniería en Informática.
