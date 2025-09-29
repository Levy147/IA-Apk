# 🚀 Cómo Ejecutar el Sistema de Tutoría Inteligente (STI)

## 📋 Prerrequisitos
- Python 3.8 o superior
- XAMPP (para MySQL)
- Git (opcional)

## 🔧 Pasos para Ejecutar

### 1. Iniciar XAMPP
1. Abre XAMPP Control Panel
2. Inicia **Apache** y **MySQL**
3. Abre phpMyAdmin (http://localhost/phpmyadmin)
4. Crea la base de datos `sti_database` con cotejamiento `utf8mb4_unicode_ci`

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv_new

# Activar entorno virtual (Windows)
venv_new\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv_new/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Migrate Flask-CORS PyMySQL SQLAlchemy cryptography python-dotenv bcrypt PyJWT Werkzeug python-dateutil pytz email-validator scikit-learn pandas numpy requests beautifulsoup4 pytest pytest-flask
```

### 4. Crear Base de Datos
```bash
# Crear la base de datos MySQL
python -c "
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='', charset='utf8mb4')
cursor = conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS sti_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
print('Base de datos creada exitosamente')
cursor.close()
conn.close()
"
```

### 5. Inicializar Base de Datos (Opcional)
```bash
# Solo si quieres datos de prueba
python init_db.py
```

### 6. Ejecutar la Aplicación
```bash
python app.py
```

## 🌐 Acceder al Sistema
- **URL**: http://localhost:5000
- **Puerto**: 5000

## 👥 Usuarios de Prueba (si ejecutaste init_db.py)
- **Administrador**: admin@sti.com / admin123
- **Docente**: profesor@sti.com / profesor123
- **Estudiantes**: estudiante1@sti.com / estudiante123

## 🔧 Comandos Útiles

### Probar el Sistema
```bash
python test_system.py
```

### Detener la Aplicación
- Presiona `Ctrl+C` en la terminal donde está ejecutándose

### Desactivar Entorno Virtual
```bash
deactivate
```

## ⚠️ Solución de Problemas

### Error de Conexión a Base de Datos
1. Verifica que XAMPP esté ejecutándose
2. Asegúrate de que MySQL esté activo
3. Comprueba que la base de datos `sti_database` existe

### Error de Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error de Puerto en Uso
- Cambia el puerto en `app.py` línea 25: `app.run(debug=True, host='0.0.0.0', port=5001)`

## 📁 Estructura del Proyecto
```
sti-proyect/
├── app/                 # Código de la aplicación
├── venv_new/           # Entorno virtual
├── uploads/            # Archivos subidos
├── app.py              # Aplicación principal
├── init_db.py          # Inicialización de BD
├── test_system.py      # Pruebas del sistema
└── requirements.txt    # Dependencias
```

## 🎯 Características del Sistema
- ✅ Sistema de autenticación
- ✅ Dashboard para estudiantes y docentes
- ✅ Examen diagnóstico personalizado
- ✅ Cuestionario VARK para estilos de aprendizaje
- ✅ Rutas de aprendizaje adaptadas
- ✅ Motor de recomendaciones con IA
- ✅ Analíticas avanzadas
- ✅ Integración con Google Forms

---
**Sistema de Tutoría Inteligente (STI)** - Desarrollado por estudiantes de la Universidad de San Carlos de Guatemala
