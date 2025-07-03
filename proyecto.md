---
marp: true
theme: default
class: center, middle
---

# 📊 Análisis Estadístico de Repositorios Académicos en GitHub  
### 🧪 Caso de Estudio: Sistema de Conversión y Organización de Documentos Técnicos en Markdown  
**👥 Integrantes:**  
- 👤 Jerson Roni Chambi Cori  
- 👤 Jaime Elias Flores Quispe  
- 👤 Elvis Ronald Leyva Sardon  
- 👤 Brian Danilo Chite Quispe 
---

# 🚨 Problemática  
## "Desorganización y falta de control en la gestión de documentación técnica académica"

📚 *Contexto:*  
En la Facultad de Ingeniería de Sistemas, los estudiantes enfrentan dificultades para:  
- 📎 Estructurar documentos técnicos  
- 🕒 Controlar versiones y rastrear cambios  
- 💡 Mejorar automáticamente sus documentos con IA  
- 📂 Mantener un flujo de trabajo organizado y accesible  

---

## ⚠️ Problemática Específica  

1. 🗃️ **Diversidad de formatos:**  
   Soporte disperso para `.doc`, `.docx`, `.pdf`, `.html`, `.txt` → difícil estandarización  
2. 🕒 **Falta de control de versiones:**  
   Cambios no registrados, sin historial estructurado  
3. 🛠️ **Procesos manuales y sin IA:**  
   Sin automatización para estructurar o mejorar documentos  

---

## 🎯 Objetivo General  

🧠 Diseñar e implementar un sistema web que facilite la **conversión automática de documentos técnicos a Markdown**, incorporando:  
- 🧾 Organización estructurada  
- 🔄 Control de versiones  
- 🤖 Mejora automatizada con IA  
- 👁️ Previsualización en tiempo real
- 🧠 Identificador de Plageo
- 🌐 Publicación en plataformas externas (GitHub)

---

## 📌 Objetivos Específicos  

---

### 🔄 1. Automatizar la conversión de documentos  

✅ Soportar archivos `.doc`, `.docx`, `.pdf`  
🧾 Convertir a Markdown conservando formato y estructura  

---

### 🗂️ 2. Implementar sistema de gestión de versiones  

🗃️ Guardar, comparar y restaurar versiones anteriores  
📈 Rastrear cambios y evolución documental  

---

### 🤖 3. Mejorar documentos con inteligencia artificial  

🧠 Sugerencias automáticas de mejora de estructura y redacción  
✨ Limpieza y enriquecimiento del contenido Markdown  

---

### 👁️ 4. Incorporar previsualización en tiempo real  

🖥️ Visualizar el documento Markdown a medida que se edita  
🎯 Evitar errores de formato o estructura  

### 🧠 5. Identificador de Plageo
📊 Calcular similitud mediante Cosine Similarity
🔍 Identificar contenido redundante o plagiado

### 🌐 6. Publicar archivo como README en GitHub
📤 Subir documento Markdown como README.md al repositorio del usuario
🔐 Usar autenticación mediante token GitHub

### 🌐 7. Publicar documentos individuales en Wiki de GitHub
📄 Permitir subir un archivo Markdown como página Wiki

### 📚 8. Publicar múltiples archivos con índice en Wiki
📂 Publicar varios archivos Markdown como páginas
🧭 Generar automáticamente página de inicio con enlaces (índice navegable)

