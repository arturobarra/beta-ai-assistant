# Beta - Asistente Virtual Local con Inteligencia Artificial

Beta es un asistente virtual desarrollado en Python como proyecto personal de aprendizaje y desarrollo.

El objetivo del proyecto es construir un asistente local capaz de interactuar mediante voz, utilizar inteligencia artificial, mantener memoria persistente, consultar documentación mediante RAG y ejecutar funciones controladas en Windows.

## Versión estable actual

**Beta v2.8.3**

## Características principales

- Reconocimiento de voz con Vosk y Faster-Whisper
- Síntesis de voz local mediante Piper
- Inteligencia artificial local con Ollama y Qwen
- Reconocimiento biométrico de hablante
- Memoria persistente mediante SQLite
- Biblioteca académica y técnica mediante RAG
- Búsqueda semántica con Sentence Transformers
- OCR de documentos PDF
- Enrutamiento inteligente de fuentes
- Detección de cambios de contexto
- Integración con Spotify
- Sistema de respaldos automáticos
- Interfaz gráfica flotante
- Procesamiento principalmente local

## Arquitectura general

Usuario  
↓  
Vosk  
↓  
Faster-Whisper  
↓  
Reconocimiento de hablante  
↓  
Router inteligente  
↓  
Biblioteca académica / Biblioteca técnica / Qwen  
↓  
Piper / Daniela

## Privacidad

Las bases de datos personales, documentos, modelos de IA, credenciales y archivos privados no forman parte de este repositorio.

## Tecnologías

Python, SQLite, Vosk, Faster-Whisper, Piper, Ollama, Qwen, Sentence Transformers, SpeechBrain, PyMuPDF, Tesseract OCR, Tkinter y Spotify Web API.

## Autor

**Jonathan Gonzalez Barra**

Proyecto desarrollado como parte de mi aprendizaje y formación en Ingeniería en Informática.