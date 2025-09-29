# Sistema de Tutoría Inteligente (STI)

Un sistema de tutoría inteligente desarrollado en Python que personaliza el aprendizaje mediante inteligencia artificial, evaluación diagnóstica y identificación de estilos de aprendizaje VARK.

## 🎯 Características Principales

- **Examen Diagnóstico Multiformal**: Evaluación automatizada con 25+ preguntas de diversos tipos
- **Identificación de Estilos de Aprendizaje**: Cuestionario VARK para personalizar la experiencia
- **Rutas de Aprendizaje Personalizadas**: Generación automática basada en IA
- **Integración con Google Forms**: Para exámenes diagnósticos
- **Base de Datos MySQL**: Con XAMPP para almacenamiento robusto
- **Interfaz Web Moderna**: Con Flask y Bootstrap
- **Analíticas Avanzadas**: Para estudiantes y docentes

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- XAMPP (para MySQL)
- Git

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd sti-proyect
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar XAMPP

1. Inicia XAMPP
2. Activa Apache y MySQL
3. Crea una base de datos llamada `sti_database` en phpMyAdmin

### 5. Configurar Variables de Entorno

```bash
# Copia el archivo de ejemplo
copy env_example.txt .env
# Edita .env con tus configuraciones
```

### 6. Inicializar la Base de Datos

```bash
python init_db.py
```

### 7. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## 👥 Usuarios de Prueba

Después de ejecutar `init_db.py`, tendrás los siguientes usuarios:

- **Administrador**: admin@sti.com / admin123
- **Docente**: profesor@sti.com / profesor123
- **Estudiantes**: estudiante1@sti.com / estudiante123

## 🏗️ Arquitectura del Sistema

### Backend
- **Flask**: Framework web principal
- **SQLAlchemy**: ORM para base de datos
- **MySQL**: Base de datos con XAMPP
- **scikit-learn**: Algoritmos de IA

### Frontend
- **Bootstrap 5**: Framework CSS
- **Chart.js**: Gráficos y analíticas
- **Font Awesome**: Iconos

### Módulos Principales

1. **Autenticación**: Login/registro de usuarios
2. **Estudiantes**: Dashboard, cursos, exámenes, rutas de aprendizaje
3. **Docentes**: Dashboard, gestión de cursos, analíticas
4. **IA**: Generación de rutas, análisis VARK, recomendaciones
5. **API**: Integración con Google Forms y servicios externos

## 📊 Funcionalidades

### Para Estudiantes
- Registro y perfil personal
- Examen diagnóstico personalizado
- Cuestionario VARK para identificar estilo de aprendizaje
- Rutas de aprendizaje adaptadas
- Seguimiento de progreso
- Recursos personalizados

### Para Docentes
- Dashboard con estadísticas
- Gestión de cursos y estudiantes
- Creación de preguntas y recursos
- Analíticas detalladas
- Seguimiento del progreso de estudiantes

### Sistema de IA
- Análisis de estilos de aprendizaje VARK
- Generación automática de rutas de aprendizaje
- Motor de recomendaciones
- Análisis de rendimiento
- Adaptación dinámica del contenido

## 🔧 Configuración Avanzada

### Integración con Google Forms

1. Crea un formulario en Google Forms
2. Obtén la API key y Form ID
3. Configura las variables en `.env`:
   ```
   GOOGLE_FORMS_API_KEY=tu-api-key
   GOOGLE_FORMS_FORM_ID=tu-form-id
   ```

### Personalización de IA

Puedes ajustar los parámetros de IA en `config.py`:
- `MIN_QUESTIONS_DIAGNOSTIC`: Mínimo de preguntas diagnósticas
- `VARK_QUESTIONS`: Número de preguntas VARK
- `MIN_MASTERY_THRESHOLD`: Umbral para considerar dominio

## 📁 Estructura del Proyecto

```
sti-proyect/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── main/           # Rutas principales
│   ├── auth/           # Autenticación
│   ├── student/        # Módulo de estudiantes
│   ├── teacher/        # Módulo de docentes
│   ├── api/            # API REST
│   ├── ai/             # Módulos de IA
│   └── templates/      # Plantillas HTML
├── uploads/            # Archivos subidos
├── models/             # Modelos de IA entrenados
├── config.py           # Configuración
├── app.py              # Aplicación principal
├── init_db.py          # Inicialización de BD
└── requirements.txt    # Dependencias
```

## 🧪 Pruebas

```bash
# Ejecutar pruebas (cuando estén implementadas)
python -m pytest tests/
```

## 📈 Roadmap

- [ ] Implementación completa de Google Forms
- [ ] Sistema de notificaciones
- [ ] Aplicación móvil
- [ ] Integración con LMS existentes
- [ ] Análisis predictivo avanzado
- [ ] Gamificación

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autores

- Herbert Steven Galeano Flores - 202406260
- José Angel Culajay Castellanos - 202501021
- Carlos David Alejandro Coronado Pérez - 202507699

## 📞 Soporte

Para soporte técnico o preguntas, contacta a: [email@ejemplo.com]

---

**Sistema de Tutoría Inteligente (STI)** - Transformando la educación con inteligencia artificial 🚀
