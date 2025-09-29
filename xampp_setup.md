# Configuración de XAMPP para el STI

## 📋 Pasos para configurar XAMPP

### 1. Descargar e Instalar XAMPP

1. Ve a [https://www.apachefriends.org/](https://www.apachefriends.org/)
2. Descarga XAMPP para Windows
3. Instala XAMPP en la ubicación por defecto (normalmente `C:\xampp`)

### 2. Iniciar XAMPP

1. Abre el Panel de Control de XAMPP
2. Inicia **Apache** (haz clic en "Start")
3. Inicia **MySQL** (haz clic en "Start")

### 3. Crear la Base de Datos

1. Abre tu navegador y ve a `http://localhost/phpmyadmin`
2. Haz clic en "Nueva" en el panel izquierdo
3. Crea una nueva base de datos llamada `sti_database`
4. Selecciona "utf8mb4_unicode_ci" como collation

### 4. Configurar Usuario MySQL (Opcional)

Por defecto, XAMPP usa:
- **Usuario**: `root`
- **Contraseña**: (vacía)

Si quieres cambiar esto:
1. En phpMyAdmin, ve a "Cuentas de usuario"
2. Edita el usuario `root`
3. Cambia la contraseña si es necesario
4. Actualiza el archivo `.env` con las nuevas credenciales

### 5. Verificar la Configuración

Ejecuta el script de prueba:
```bash
python test_system.py
```

## 🔧 Configuración del Archivo .env

Crea un archivo `.env` en la raíz del proyecto con:

```env
# Configuración de la base de datos MySQL (XAMPP)
DEV_DATABASE_URL=mysql+pymysql://root:@localhost:3306/sti_database
DATABASE_URL=mysql+pymysql://root:@localhost:3306/sti_database_prod

# Si cambiaste la contraseña de MySQL:
# DEV_DATABASE_URL=mysql+pymysql://root:tu_contraseña@localhost:3306/sti_database
```

## 🚨 Solución de Problemas Comunes

### Error: "Can't connect to MySQL server"

**Solución:**
1. Verifica que MySQL esté ejecutándose en XAMPP
2. Verifica que el puerto 3306 esté libre
3. Reinicia XAMPP

### Error: "Access denied for user 'root'"

**Solución:**
1. Verifica las credenciales en el archivo `.env`
2. Si cambiaste la contraseña, actualiza el archivo `.env`
3. Asegúrate de que el usuario `root` tenga permisos

### Error: "Unknown database 'sti_database'"

**Solución:**
1. Ve a phpMyAdmin
2. Crea la base de datos `sti_database`
3. Ejecuta `python init_db.py` para inicializar las tablas

### Puerto 3306 en uso

**Solución:**
1. Abre el Administrador de tareas
2. Busca procesos que usen el puerto 3306
3. Termina esos procesos
4. Reinicia XAMPP

## 📊 Verificar que Todo Funciona

1. **XAMPP ejecutándose:**
   - Apache: ✅ Verde
   - MySQL: ✅ Verde

2. **Base de datos creada:**
   - Ve a `http://localhost/phpmyadmin`
   - Deberías ver `sti_database` en la lista

3. **Sistema funcionando:**
   ```bash
   python test_system.py
   ```
   - Debería mostrar "Todas las pruebas pasaron"

4. **Aplicación web:**
   ```bash
   python app.py
   ```
   - Ve a `http://localhost:5000`

## 🔄 Comandos Útiles

```bash
# Inicializar base de datos
python init_db.py

# Probar sistema
python test_system.py

# Ejecutar aplicación
python app.py

# Instalar dependencias
pip install -r requirements.txt
```

## 📞 Soporte

Si tienes problemas con XAMPP:
1. Revisa los logs de XAMPP en `C:\xampp\apache\logs\` y `C:\xampp\mysql\data\`
2. Verifica que no haya conflictos de puertos
3. Reinicia XAMPP completamente
4. Consulta la documentación oficial de XAMPP
