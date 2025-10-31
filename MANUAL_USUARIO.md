# Manual de Usuario - Sistema de Tutoría Inteligente (STI)

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Guía para Estudiantes](#guía-para-estudiantes)
4. [Guía para Profesores](#guía-para-profesores)
5. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

El **Sistema de Tutoría Inteligente (STI)** es una plataforma educativa que personaliza tu experiencia de aprendizaje adaptándose a tu estilo de aprendizaje único. El sistema utiliza inteligencia artificial para:

- Identificar tu estilo de aprendizaje (Visual, Auditivo, Lectura/Escritura o Kinestésico)
- Evaluar tus conocimientos previos mediante exámenes diagnósticos
- Crear rutas de aprendizaje personalizadas
- Recomendar recursos educativos adaptados a ti
- Seguir tu progreso y ayudarte a alcanzar tus objetivos

---

## Acceso al Sistema

### Requisitos

- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Conexión a internet
- Cuenta de usuario (estudiante o profesor)

### Dirección Web

Abre tu navegador y accede a:
```
http://localhost:5000
```

### Iniciar Sesión

1. En la página principal, haz clic en **"Iniciar Sesión"** o ve directamente a la página de login
2. Ingresa tu **correo electrónico** y **contraseña**
3. Haz clic en **"Iniciar Sesión"**

### Registrarse (Nuevos Usuarios)

1. En la página de inicio, haz clic en **"Registrarse"**
2. Completa el formulario:
   - **Correo electrónico**: Tu email
   - **Contraseña**: Crea una contraseña segura
   - **Confirmar contraseña**: Repite tu contraseña
   - **Nombre**: Tu primer nombre
   - **Apellido**: Tu apellido
   - **Tipo de usuario**: Selecciona "Estudiante" o "Profesor"
   
   **Si eres Estudiante:**
   - **Código de estudiante**: Tu número de matrícula
   - **Nivel**: Tu nivel educativo (ej: universidad)
   - **Institución**: Nombre de tu escuela/universidad
   
   **Si eres Profesor:**
   - **Código de profesor**: Tu código identificador
   - **Departamento**: Departamento académico
   - **Especialización**: Tu área de especialización

3. Haz clic en **"Registrarse"**
4. Serás redirigido al login para iniciar sesión

### Cerrar Sesión

Para cerrar sesión, haz clic en tu nombre de usuario (esquina superior derecha) y selecciona **"Cerrar Sesión"**.

---

## Guía para Estudiantes

### Dashboard del Estudiante

Al iniciar sesión como estudiante, accederás al dashboard que muestra:

- **Cursos activos**: Cursos en los que estás matriculado
- **Progreso general**: Porcentaje promedio de avance
- **Exámenes diagnósticos completados**: Número de diagnósticos realizados
- **Rutas de aprendizaje activas**: Rutas personalizadas generadas
- **Perfil VARK**: Tu estilo de aprendizaje identificado

### Proceso de Configuración Inicial

#### Paso 1: Completar el Cuestionario VARK

El cuestionario VARK identifica tu estilo de aprendizaje. Es fundamental completarlo para personalizar tu experiencia.

1. Desde el dashboard, busca la sección **"Cuestionario de Estilos de Aprendizaje"**
2. Haz clic en **"Completar Cuestionario VARK"**
3. Responde cada pregunta seleccionando la opción que mejor te represente:
   - **V (Visual)**: Prefieres ver diagramas, gráficos, imágenes
   - **A (Auditivo)**: Prefieres escuchar explicaciones, discusiones
   - **R (Lectura/Escritura)**: Prefieres leer textos, tomar notas
   - **K (Kinestésico)**: Prefieres hacer actividades prácticas, experimentos

4. Completa todas las preguntas (generalmente 16)
5. Haz clic en **"Enviar"**

**Nota**: También puedes acceder a un formulario externo de Google Forms si está configurado. El sistema te mostrará el enlace correspondiente.

#### Paso 2: Seleccionar Cursos

Después de completar el VARK:

1. Serás redirigido a la página de **"Selección de Cursos"**
2. Verás una lista de cursos disponibles
3. Tu estilo de aprendizaje identificado se mostrará en la parte superior
4. Selecciona los cursos en los que deseas matricularte haciendo clic en **"Matricularme"**

#### Paso 3: Realizar Examen Diagnóstico

Para cada curso seleccionado:

1. El sistema te pedirá completar un **examen diagnóstico**
2. Este examen evalúa tus conocimientos previos en el tema
3. Haz clic en **"Realizar Examen Diagnóstico"**
4. Responde todas las preguntas con sinceridad
5. Al finalizar, se mostrará tu calificación
6. Con base en tus resultados, el sistema generará una ruta de aprendizaje personalizada

### Navegación por Cursos

#### Ver Todos los Cursos

1. En el menú, haz clic en **"Todos los Cursos"**
2. Verás una lista completa de cursos disponibles
3. Para cada curso puedes ver:
   - Nombre y descripción
   - Profesor responsable
   - Créditos
   - Estado (activo/inactivo)

#### Ver Mis Cursos

1. Haz clic en **"Mis Cursos"** en el menú
2. Verás solo los cursos en los que estás matriculado
3. Cada curso muestra:
   - Progreso actual
   - Estado de matrícula
   - Acciones disponibles

#### Detalle de Curso

1. Haz clic en el nombre de un curso para ver su detalle
2. Verás información completa:
   - Descripción del curso
   - Competencias a desarrollar
   - Tu progreso
   - Estado del examen diagnóstico
   - Ruta de aprendizaje generada (si existe)
   - Recursos disponibles

### Ruta de Aprendizaje Personalizada

La ruta de aprendizaje es una secuencia personalizada de pasos diseñada específicamente para ti:

1. Accede a **"Mi Ruta de Aprendizaje"** desde el detalle del curso
2. Verás una secuencia de pasos ordenados
3. Cada paso incluye:
   - Competencia a desarrollar
   - Recursos recomendados (adaptados a tu estilo VARK)
   - Estado (pendiente, en progreso, completado)
   - Progreso individual

4. Marca los pasos como completados conforme avanzas
5. El sistema ajustará la ruta según tu progreso

### Recursos de Aprendizaje

Los recursos están adaptados a tu estilo de aprendizaje:

#### Tipos de Recursos

- **Videos**: Para estudiantes visuales y auditivos
- **Lecturas**: Para estudiantes de lectura/escritura
- **Ejercicios**: Para práctica y refuerzo
- **Simulaciones**: Para estudiantes kinestésicos y visuales
- **Audio**: Para estudiantes auditivos

#### Acceder a Recursos

1. Desde el detalle del curso, ve a **"Recursos"**
2. Los recursos están organizados por competencia
3. Cada recurso muestra:
   - Título y descripción
   - Tipo de recurso
   - Duración estimada
   - Adecuación a tu estilo VARK (indicador visual)

4. Haz clic en el recurso para acceder
5. Algunos recursos pueden estar en Google Drive (enlaces externos)

### Seguimiento de Progreso

#### Ver Progreso General

1. En el dashboard, observa el **"Progreso General"**
2. Este porcentaje refleja tu avance promedio en todos los cursos activos

#### Ver Progreso por Curso

1. En el detalle de cada curso, verás tu progreso específico
2. Puedes ver:
   - Progreso general del curso
   - Progreso por competencia
   - Calificaciones obtenidas
   - Tiempo invertido

#### Ver Mi Perfil

1. Haz clic en **"Mi Perfil"** en el menú
2. Verás:
   - Información personal
   - Perfil VARK completo:
     - Puntajes por estilo (Visual, Auditivo, Lectura, Kinestésico)
     - Estilo dominante
     - Recomendaciones basadas en tu estilo
   - Estadísticas de aprendizaje:
     - Cursos completados
     - Rutas de aprendizaje activas
     - Progreso general
   - Historial de actividad

### Unidades del Curso

1. En el detalle del curso, haz clic en **"Ver Unidades"**
2. Verás las unidades organizadas del curso
3. Cada unidad puede tener enlaces a recursos en Google Drive
4. Navega por las unidades en orden recomendado

---

## Guía para Profesores

### Dashboard del Profesor

Al iniciar sesión como profesor, accederás a un dashboard con:

- **Mis Cursos**: Lista de cursos que impartes
- **Total de Estudiantes**: Número total de estudiantes en tus cursos
- **Exámenes Diagnósticos**: Total y completados
- **Progreso Promedio**: Promedio de progreso de todos tus estudiantes

### Gestionar Cursos

#### Ver Mis Cursos

1. En el menú, haz clic en **"Mis Cursos"**
2. Verás todos los cursos que has creado
3. Para cada curso puedes ver:
   - Nombre y código
   - Número de estudiantes matriculados
   - Progreso promedio
   - Estado

#### Crear Nuevo Curso

1. En el dashboard o desde "Mis Cursos", haz clic en **"Crear Curso"**
2. Completa el formulario:
   - **Nombre del curso**: Nombre completo
   - **Código**: Código identificador (ej: MATH-BAS-1)
   - **Descripción**: Descripción del curso
   - **Materia**: Área de conocimiento
   - **Nivel**: Nivel educativo
   - **Créditos**: Número de créditos
   - **Requiere diagnóstico**: Marcar si los estudiantes deben hacer examen diagnóstico
   - **Preguntas mínimas**: Mínimo de preguntas para el diagnóstico

3. Haz clic en **"Crear Curso"**
4. Serás redirigido al detalle del curso creado

#### Ver Detalle de Curso

1. Haz clic en el nombre de un curso
2. Verás:
   - Información completa del curso
   - Lista de estudiantes matriculados
   - Estadísticas del curso:
     - Total de estudiantes
     - Exámenes diagnósticos completados
     - Progreso promedio

### Gestionar Estudiantes

#### Ver Estudiantes de un Curso

1. Desde el detalle del curso, haz clic en **"Ver Estudiantes"**
2. Verás una lista completa con:
   - Nombre del estudiante
   - Código de estudiante
   - Progreso individual
   - Estado del examen diagnóstico
   - Estilo de aprendizaje VARK
   - Ruta de aprendizaje (si tiene)

#### Ver Progreso de un Estudiante

1. Desde la lista de estudiantes, haz clic en el nombre de un estudiante
2. Verás información detallada:
   - Perfil completo del estudiante
   - Progreso en cada competencia
   - Calificaciones obtenidas
   - Rutas de aprendizaje activas
   - Historial de actividad

### Analíticas y Reportes

#### Ver Analíticas

1. En el menú, haz clic en **"Analíticas"**
2. Verás gráficos y estadísticas:
   - **Progreso por curso**: Gráfico de progreso promedio por curso
   - **Distribución de estilos VARK**: Cuántos estudiantes tienen cada estilo
   - **Completitud de diagnósticos**: Porcentaje de estudiantes que completaron el diagnóstico
   - **Rendimiento general**: Tendencias y estadísticas

#### Exportar Reportes

1. Desde la página de analíticas, algunas secciones pueden tener opción de exportar
2. Los reportes se pueden exportar en formato PDF o Excel (según implementación)

### Configurar Exámenes Diagnósticos

Los exámenes diagnósticos pueden configurarse de dos formas:

#### Método 1: Formularios Externos (Google Forms)

1. Crea un formulario en Google Forms
2. Configura las preguntas del examen
3. Haz el formulario público o comparte el enlace
4. Obtén el ID del formulario desde la URL
5. Actualiza la configuración en el código (requiere acceso técnico)

#### Método 2: Preguntas en el Sistema

1. Desde el detalle del curso, ve a **"Gestionar Preguntas"** (si está disponible)
2. Agrega preguntas del examen diagnóstico
3. Para cada pregunta configura:
   - Texto de la pregunta
   - Tipo (opción múltiple, verdadero/falso, etc.)
   - Dificultad
   - Opciones de respuesta
   - Respuesta correcta
   - Explicación

### Configurar Recursos

1. Desde el detalle del curso, ve a **"Recursos"**
2. Haz clic en **"Agregar Recurso"**
3. Completa la información:
   - **Título**: Nombre del recurso
   - **Descripción**: Descripción breve
   - **Tipo**: Video, lectura, ejercicio, simulación, audio
   - **URL**: Enlace al recurso (si es externo)
   - **Texto**: Contenido (si es texto)
   - **Competencia**: Competencia relacionada
   - **Dificultad**: Nivel de dificultad
   - **Duración**: Tiempo estimado en minutos
   - **Puntajes VARK**: Indica qué tan adecuado es el recurso para cada estilo:
     - Visual (0.0 a 1.0)
     - Auditivo (0.0 a 1.0)
     - Lectura (0.0 a 1.0)
     - Kinestésico (0.0 a 1.0)

4. Haz clic en **"Guardar"**

**Ejemplo de Puntajes VARK:**
- Video educativo: Visual=0.9, Auditivo=0.8, Lectura=0.3, Kinestésico=0.2
- Ejercicio práctico: Visual=0.4, Auditivo=0.2, Lectura=0.6, Kinestésico=0.9

---

## Preguntas Frecuentes

### Para Estudiantes

#### ¿Puedo cambiar mi estilo de aprendizaje después de completar el VARK?

Sí, puedes actualizar manualmente tu estilo dominante desde tu perfil. Sin embargo, se recomienda completar el cuestionario nuevamente para obtener resultados más precisos.

#### ¿Qué pasa si no completo el examen diagnóstico?

Dependiendo de la configuración del curso, es posible que no puedas acceder a ciertos recursos o a la ruta de aprendizaje personalizada hasta completarlo.

#### ¿Cómo sé qué recursos son mejores para mí?

Los recursos están marcados con indicadores que muestran su adecuación a tu estilo VARK. Los recursos con mayor puntaje para tu estilo aparecerán primero y se recomendarán automáticamente.

#### ¿Puedo acceder a recursos de otros estilos de aprendizaje?

Sí, aunque el sistema prioriza recursos adaptados a tu estilo, puedes acceder a todos los recursos disponibles para tener una experiencia más completa.

#### ¿Cómo se genera mi ruta de aprendizaje?

La ruta se genera automáticamente después de:
1. Completar el cuestionario VARK
2. Realizar el examen diagnóstico
3. El sistema analiza tus resultados y crea una secuencia personalizada de competencias y recursos

#### ¿Puedo modificar mi ruta de aprendizaje?

La ruta se ajusta automáticamente según tu progreso. Si necesitas cambios específicos, contacta a tu profesor.

### Para Profesores

#### ¿Cómo agrego estudiantes a un curso?

Los estudiantes se matriculan automáticamente cuando seleccionan tu curso desde su dashboard. No necesitas agregarlos manualmente.

#### ¿Puedo ver las respuestas individuales del examen diagnóstico?

Desde el detalle del curso y la lista de estudiantes, puedes ver el estado del diagnóstico de cada estudiante. Para ver respuestas específicas, accede al perfil del estudiante (si está implementado).

#### ¿Cómo configuro competencias para un curso?

Las competencias se configuran desde el detalle del curso en la sección "Competencias" (si está disponible en la interfaz, o requiere configuración técnica).

#### ¿Los recursos deben estar almacenados en el sistema?

No necesariamente. Puedes enlazar recursos externos (videos de YouTube, documentos en Google Drive, etc.) usando la URL del recurso.

#### ¿Cómo funciona la generación automática de rutas?

El sistema usa los datos del perfil VARK y resultados del diagnóstico para crear una secuencia personalizada. Los algoritmos consideran:
- Dificultad inicial detectada
- Estilo de aprendizaje
- Recursos disponibles
- Prerequisitos entre competencias

---

## Consejos de Uso

### Para Estudiantes

1. **Completa el VARK con honestidad**: Tus respuestas determinan las recomendaciones
2. **Realiza los diagnósticos seriamente**: Ayudan a crear rutas más precisas
3. **Sigue tu ruta de aprendizaje**: Está diseñada específicamente para ti
4. **Marca tu progreso**: Actualiza el estado de los pasos completados
5. **Explora diferentes recursos**: Aunque están adaptados, experimenta con diversos formatos

### Para Profesores

1. **Configura bien los recursos**: Los puntajes VARK son importantes para las recomendaciones
2. **Revisa las analíticas regularmente**: Te ayudan a identificar estudiantes que necesitan apoyo
3. **Actualiza el contenido**: Mantén los recursos actualizados y relevantes
4. **Comunícate con los estudiantes**: El sistema es una herramienta, la comunicación es clave

---

## Soporte y Ayuda

Si encuentras problemas o tienes preguntas:

1. **Revisa este manual**: La mayoría de las dudas comunes están cubiertas
2. **Contacta a tu profesor**: Para problemas específicos del curso
3. **Soporte técnico**: Para problemas técnicos del sistema, contacta al administrador

---

**Versión del Manual**: 1.0  
**Última Actualización**: 2025  
**Sistema**: STI v1.0

