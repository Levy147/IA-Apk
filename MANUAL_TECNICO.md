# Manual Técnico - Sistema de Tutoría Inteligente (STI)

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Requisitos del Sistema](#requisitos-del-sistema)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Base de Datos](#base-de-datos)
8. [Configuración de Google Forms](#configuración-de-google-forms)
9. [API y Endpoints](#api-y-endpoints)
10. [Sistema de Inteligencia Artificial](#sistema-de-inteligencia-artificial)
11. [Despliegue](#despliegue)
12. [Mantenimiento](#mantenimiento)
13. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

El **Sistema de Tutoría Inteligente (STI)** es una plataforma web educativa desarrollada en Python utilizando el framework Flask. El sistema permite personalizar la experiencia de aprendizaje de los estudiantes mediante:

- Análisis de estilos de aprendizaje VARK (Visual, Auditivo, Lectura/Escritura, Kinestésico)
- Exámenes diagnósticos para evaluar conocimientos previos
- Generación automática de rutas de aprendizaje personalizadas
- Recomendación de recursos educativos adaptados al perfil del estudiante
- Seguimiento de progreso y analíticas

---

## Arquitectura del Sistema

### Arquitectura General

El STI sigue una arquitectura **Modelo-Vista-Controlador (MVC)** con los siguientes componentes:

```
┌─────────────────────────────────────────┐
│         Cliente Web (Navegador)        │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Flask Application Layer         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Routes   │  │ Forms    │  │ Templates│
│  └────┬─────┘  └────┬─────┘  └────┬────┘│
│       │             │             │     │
│  ┌────▼─────────────▼─────────────▼────┐│
│  │         Business Logic               ││
│  └────┬────────────────────────────────┘│
│       │                                  │
┌───────▼──────────────────────────────────┐
│      Models (SQLAlchemy ORM)             │
└───────┬──────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│      Base de Datos MySQL (XAMPP)         │
└───────────────────────────────────────────┘
```

### Componentes Principales

1. **Frontend**: Templates HTML con Jinja2
2. **Backend**: Flask (Python)
3. **Base de Datos**: MySQL (a través de XAMPP)
4. **Autenticación**: Flask-Login
5. **IA/ML**: scikit-learn, pandas, numpy para análisis VARK y generación de rutas

---

## Tecnologías Utilizadas

### Backend

- **Python 3.12**: Lenguaje de programación principal
- **Flask 2.3.3**: Framework web
- **Flask-SQLAlchemy 3.0.5**: ORM para base de datos
- **Flask-Login 0.6.3**: Gestión de sesiones de usuario
- **Flask-WTF 1.1.1**: Manejo de formularios
- **Flask-Migrate 4.0.5**: Migraciones de base de datos
- **Flask-CORS 4.0.0**: Soporte CORS para APIs

### Base de Datos

- **MySQL**: Motor de base de datos
- **PyMySQL 1.1.0**: Driver Python para MySQL
- **SQLAlchemy 2.0.21**: ORM

### Inteligencia Artificial y Análisis

- **scikit-learn 1.3.0**: Machine Learning
- **pandas 2.0.3**: Procesamiento de datos
- **numpy 1.24.3**: Cálculos numéricos
- **scipy 1.11.1**: Funciones científicas

### Utilidades

- **requests 2.31.0**: Peticiones HTTP (integración con Google Forms)
- **beautifulsoup4 4.12.2**: Parsing HTML
- **bcrypt 4.0.1**: Encriptación de contraseñas
- **python-dotenv 1.0.0**: Variables de entorno

---

## Requisitos del Sistema

### Requisitos Mínimos

- **Sistema Operativo**: Windows 10/11, Linux, macOS
- **Python**: 3.9 o superior (recomendado 3.12)
- **RAM**: 4GB mínimo (8GB recomendado)
- **Espacio en disco**: 2GB libres
- **XAMPP**: Para base de datos MySQL
- **Navegador**: Chrome, Firefox, Edge (últimas versiones)

### Software Requerido

1. **Python 3.12** con pip
2. **XAMPP** (incluye MySQL y phpMyAdmin)
3. **Git** (opcional, para control de versiones)
4. **Editor de código** (VS Code, PyCharm, etc.)

---

## Instalación y Configuración

### Paso 1: Instalar Python

1. Descargar Python 3.12 desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marcar "Add Python to PATH"
3. Verificar instalación:
```bash
python --version
pip --version
```

### Paso 2: Instalar XAMPP

1. Descargar XAMPP desde [apachefriends.org](https://www.apachefriends.org/)
2. Instalar XAMPP en la ubicación predeterminada (normalmente `C:\xampp`)
3. Iniciar XAMPP Control Panel
4. Iniciar los servicios **Apache** y **MySQL**

### Paso 3: Configurar Base de Datos

1. Abrir phpMyAdmin: `http://localhost/phpmyadmin`
2. Crear una nueva base de datos llamada `sti_database`:
```sql
CREATE DATABASE sti_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
3. Opcional: Crear usuario específico para la aplicación

### Paso 4: Configurar el Entorno Virtual

1. Navegar al directorio del proyecto:
```bash
cd "H:\TEI Proyect\proyect TEI"
```

2. Crear entorno virtual (si no existe):
```bash
python -m venv venv_new
```

3. Activar entorno virtual:
   - **Windows**:
   ```bash
   venv_new\Scripts\activate
   ```
   - **Linux/macOS**:
   ```bash
   source venv_new/bin/activate
   ```

### Paso 5: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 6: Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto (opcional):

```env
SECRET_KEY=tu-clave-secreta-aqui
DEV_DATABASE_URL=mysql+pymysql://root:@localhost:3306/sti_database
FLASK_CONFIG=development
```

### Paso 7: Inicializar Base de Datos

Ejecutar el script de inicialización:

```bash
python init_db.py
```

Este script creará:
- Todas las tablas necesarias
- Usuarios de ejemplo (admin, profesor, estudiantes)
- Cursos de muestra
- Competencias y recursos de ejemplo

### Paso 8: Iniciar la Aplicación

**Opción 1: Usando el script batch (Windows)**
```bash
EJECUTAR.bat
```

**Opción 2: Usando Python directamente**
```bash
python iniciar.py
```

**Opción 3: Usando Flask directamente**
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

---

## Estructura del Proyecto

```
proyect-TEI/
│
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py              # Factory de la app Flask
│   │
│   ├── ai/                      # Módulos de Inteligencia Artificial
│   │   ├── analytics_engine.py          # Motor de analíticas
│   │   ├── google_forms_integration.py  # Integración con Google Forms
│   │   ├── learning_path_generator.py   # Generador de rutas de aprendizaje
│   │   ├── recommendation_engine.py      # Motor de recomendaciones
│   │   ├── vark_analyzer.py              # Analizador VARK
│   │   └── vark_forms_integration.py      # Integración VARK con Forms
│   │
│   ├── api/                     # API REST
│   │   ├── __init__.py
│   │   └── routes.py            # Rutas de la API
│   │
│   ├── auth/                    # Autenticación
│   │   ├── __init__.py
│   │   ├── forms.py             # Formularios de login/registro
│   │   └── routes.py            # Rutas de autenticación
│   │
│   ├── main/                    # Rutas principales
│   │   ├── __init__.py
│   │   └── routes.py            # Página principal, about, etc.
│   │
│   ├── models/                  # Modelos de base de datos
│   │   ├── __init__.py
│   │   ├── ai.py                # Modelos relacionados con IA
│   │   ├── assessment.py        # Modelos de evaluación
│   │   ├── course.py            # Modelos de cursos
│   │   ├── learning.py          # Modelos de aprendizaje
│   │   ├── progress.py          # Modelos de progreso
│   │   └── user.py              # Modelos de usuario
│   │
│   ├── student/                 # Módulo de estudiantes
│   │   ├── __init__.py
│   │   ├── forms.py             # Formularios de estudiantes
│   │   └── routes.py            # Rutas de estudiantes
│   │
│   ├── teacher/                 # Módulo de profesores
│   │   ├── __init__.py
│   │   ├── forms.py             # Formularios de profesores
│   │   └── routes.py            # Rutas de profesores
│   │
│   ├── static/                  # Archivos estáticos
│   │   ├── css/                 # Hojas de estilo
│   │   ├── images/              # Imágenes
│   │   └── js/                  # JavaScript
│   │
│   ├── templates/               # Plantillas HTML (Jinja2)
│   │   ├── auth/                # Templates de autenticación
│   │   ├── base.html            # Template base
│   │   ├── errors/              # Páginas de error
│   │   ├── index.html           # Página principal
│   │   ├── student/             # Templates de estudiantes
│   │   └── teacher/             # Templates de profesores
│   │
│   ├── drive_config.py          # Configuración de Google Drive
│   └── main.py                  # Punto de entrada alternativo
│
├── models/                      # Directorio para modelos ML (opcional)
│
├── uploads/                     # Archivos subidos por usuarios
│
├── venv_new/                    # Entorno virtual Python
│
├── app.py                       # Archivo principal de ejecución
├── config.py                    # Configuración de la aplicación
├── init_db.py                   # Script de inicialización de BD
├── iniciar.py                   # Script simplificado de inicio
├── run_app.py                   # Script alternativo de ejecución
├── EJECUTAR.bat                 # Script batch para Windows
├── requirements.txt             # Dependencias del proyecto
└── MANUAL_TECNICO.md            # Este archivo
```

---

## Base de Datos

### Modelo de Datos

El sistema utiliza las siguientes tablas principales:

#### Usuarios y Perfiles

- **users**: Información básica de usuarios
- **students**: Perfil extendido de estudiantes
- **teachers**: Perfil extendido de profesores

#### Cursos y Contenido

- **courses**: Cursos disponibles
- **course_enrollments**: Matrículas de estudiantes en cursos
- **competencies**: Competencias por curso
- **competency_mastery**: Dominio de competencias por estudiante

#### Evaluación

- **questions**: Preguntas de exámenes
- **diagnostic_exams**: Exámenes diagnósticos
- **vark_questions**: Preguntas del cuestionario VARK
- **vark_responses**: Respuestas VARK de estudiantes

#### Aprendizaje

- **learning_paths**: Rutas de aprendizaje personalizadas
- **learning_path_steps**: Pasos individuales de cada ruta
- **resources**: Recursos educativos (videos, ejercicios, etc.)
- **progress**: Registro de progreso de estudiantes

### Configuración de la Base de Datos

La conexión a la base de datos se configura en `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:contraseña@localhost:3306/sti_database'
```

Para desarrollo con XAMPP (usuario root sin contraseña):
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/sti_database'
```

### Migraciones

Para crear migraciones:
```bash
flask db migrate -m "Descripción del cambio"
```

Para aplicar migraciones:
```bash
flask db upgrade
```

---

## Configuración de Google Forms

El sistema integra formularios externos de Google Forms para:

1. **Cuestionario VARK**: Identificación de estilos de aprendizaje
2. **Exámenes diagnósticos**: Evaluación por curso

### Configuración en `config.py`

```python
# Formulario VARK
VARK_FORM_ID = '1FAIpQLSf9eQT1ZEn_NncQiLdsvej-HZVQuFzjAYkqQU1UV4ORl-Lg9A'
VARK_FORM_URL = 'https://docs.google.com/forms/d/e/.../viewform'

# Formularios de diagnóstico por curso
DIAGNOSTIC_FORMS = {
    'quimica': 'https://docs.google.com/forms/d/e/.../viewform',
    'tecnica_complementaria': 'https://docs.google.com/forms/d/e/.../viewform',
    'humanistica': 'https://docs.google.com/forms/d/e/.../viewform',
    'matematica': 'https://docs.google.com/forms/d/e/.../viewform'
}
```

### Configurar un Nuevo Formulario

1. Crear el formulario en Google Forms
2. Obtener el ID del formulario desde la URL
3. Hacer el formulario público o configurar acceso
4. Actualizar `config.py` con el nuevo ID/URL

---

## API y Endpoints

### Endpoints Públicos

- `GET /`: Página principal
- `GET /auth/login`: Formulario de login
- `POST /auth/login`: Autenticación
- `GET /auth/register`: Formulario de registro
- `POST /auth/register`: Registro de nuevo usuario

### Endpoints de Estudiante (requieren autenticación)

- `GET /student/dashboard`: Dashboard del estudiante
- `GET /student/profile`: Perfil del estudiante
- `GET /student/courses`: Lista de cursos
- `GET /student/course/<id>`: Detalle de curso
- `GET /student/diagnostic/<course_id>`: Examen diagnóstico
- `GET /student/vark-questionnaire`: Cuestionario VARK
- `GET /student/learning-path/<id>`: Ruta de aprendizaje

### Endpoints de Profesor (requieren autenticación)

- `GET /teacher/dashboard`: Dashboard del profesor
- `GET /teacher/courses`: Lista de cursos del profesor
- `GET /teacher/course/<id>`: Detalle de curso
- `GET /teacher/course/<id>/students`: Estudiantes del curso
- `GET /teacher/analytics`: Analíticas y reportes

### API REST

- `GET /api/stats`: Estadísticas generales
- `POST /api/learning-path/generate`: Generar ruta de aprendizaje
- `POST /api/progress/update`: Actualizar progreso
- `POST /api/vark/analyze`: Analizar respuestas VARK
- `GET /api/recommendations/<student_id>`: Recomendaciones

---

## Sistema de Inteligencia Artificial

### Módulos de IA

#### 1. VARK Analyzer (`app/ai/vark_analyzer.py`)

Analiza las respuestas del cuestionario VARK y determina el estilo de aprendizaje dominante del estudiante.

**Funcionalidades:**
- Cálculo de puntajes para cada estilo (Visual, Auditivo, Lectura, Kinestésico)
- Identificación del estilo dominante
- Generación de recomendaciones basadas en el perfil

#### 2. Learning Path Generator (`app/ai/learning_path_generator.py`)

Genera rutas de aprendizaje personalizadas basadas en:
- Perfil VARK del estudiante
- Resultados del examen diagnóstico
- Competencias del curso

**Algoritmo:**
1. Analiza el perfil VARK del estudiante
2. Evalúa el dominio inicial de competencias
3. Ordena competencias por dificultad y prerequisitos
4. Selecciona recursos adaptados al estilo de aprendizaje
5. Genera secuencia de pasos personalizada

#### 3. Recommendation Engine (`app/ai/recommendation_engine.py`)

Recomienda recursos educativos basados en:
- Estilo de aprendizaje VARK
- Progreso actual del estudiante
- Competencias a dominar
- Recursos disponibles

#### 4. Analytics Engine (`app/ai/analytics_engine.py`)

Procesa datos para generar:
- Estadísticas de progreso
- Análisis de estilos de aprendizaje
- Tendencias de desempeño
- Reportes para profesores

### Ponderación de Recursos por Estilo VARK

Los recursos tienen puntajes VARK que indican qué tan adecuados son para cada estilo:

```python
resource.visual_score = 0.9      # Muy adecuado para visuales
resource.auditory_score = 0.8     # Muy adecuado para auditivos
resource.reading_score = 0.3      # Poco adecuado para lectura
resource.kinesthetic_score = 0.2  # Poco adecuado para kinestésicos
```

El sistema prioriza recursos con puntajes altos para el estilo dominante del estudiante.

---

## Despliegue

### Desarrollo Local

El sistema está configurado para desarrollo local con:
- Flask en modo debug
- Base de datos local (XAMPP)
- Sin SSL (HTTP)

### Producción

Para desplegar en producción:

1. **Configurar variables de entorno:**
```bash
export FLASK_CONFIG=production
export SECRET_KEY=clave-secreta-fuerte
export DATABASE_URL=mysql+pymysql://user:pass@host:3306/sti_database
```

2. **Desactivar modo debug:**
En `config.py`, cambiar:
```python
class ProductionConfig(Config):
    DEBUG = False
```

3. **Usar servidor WSGI:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Configurar servidor web (Nginx/Apache):**
- Proxy reverso hacia Gunicorn
- Servir archivos estáticos directamente
- Configurar SSL/HTTPS

5. **Base de datos:**
- Usar MySQL/MariaDB en servidor dedicado
- Configurar backups automáticos
- Optimizar índices

### Recomendaciones de Seguridad

- Cambiar `SECRET_KEY` por una clave fuerte y única
- Usar contraseñas seguras para la base de datos
- Habilitar HTTPS/SSL
- Configurar firewall
- Implementar rate limiting
- Realizar backups regulares

---

## Mantenimiento

### Backups de Base de Datos

**Manual (usando mysqldump):**
```bash
mysqldump -u root -p sti_database > backup_$(date +%Y%m%d).sql
```

**Restaurar:**
```bash
mysql -u root -p sti_database < backup_YYYYMMDD.sql
```

### Limpieza de Archivos Temporales

Eliminar periódicamente archivos en:
- `uploads/`: Archivos subidos por usuarios
- `__pycache__/`: Caché de Python

### Actualización de Dependencias

1. Revisar actualizaciones:
```bash
pip list --outdated
```

2. Actualizar archivo requirements:
```bash
pip freeze > requirements.txt
```

3. Probar en entorno de desarrollo antes de producción

### Logs

El sistema registra información en:
- Consola (desarrollo)
- Archivo de log (producción, configurar en logging)

---

## Solución de Problemas

### Problema: No se conecta a la base de datos

**Solución:**
1. Verificar que MySQL esté corriendo en XAMPP
2. Verificar credenciales en `config.py`
3. Verificar que la base de datos exista:
```sql
SHOW DATABASES;
```

### Problema: Error de importación de módulos

**Solución:**
1. Activar entorno virtual:
```bash
venv_new\Scripts\activate  # Windows
source venv_new/bin/activate  # Linux/macOS
```

2. Reinstalar dependencias:
```bash
pip install -r requirements.txt
```

### Problema: Puerto 5000 en uso

**Solución:**
1. Cambiar puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

2. O cerrar proceso que usa el puerto

### Problema: Error al crear tablas

**Solución:**
1. Verificar permisos de usuario MySQL
2. Verificar que la base de datos exista
3. Ejecutar manualmente:
```python
python init_db.py
```

### Problema: Formularios VARK no funcionan

**Solución:**
1. Verificar que las URLs en `config.py` sean correctas
2. Verificar que los formularios de Google Forms sean públicos
3. Revisar integración en `app/ai/vark_forms_integration.py`

---

## Contacto y Soporte

Para soporte técnico o consultas sobre la implementación, contactar al equipo de desarrollo.

---

**Versión del Manual**: 1.0  
**Última Actualización**: 2025  
**Sistema**: STI v1.0

