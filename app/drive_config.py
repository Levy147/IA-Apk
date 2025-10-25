"""
Configuración de enlaces a Google Drive por curso
Basado en: https://drive.google.com/drive/folders/1650yAVCLmN7zDJTITp_kZRD2n63Q4k1p?usp=drive_link
"""

# Carpeta principal de recursos
MAIN_DRIVE_FOLDER = "https://drive.google.com/drive/folders/1650yAVCLmN7zDJTITp_kZRD2n63Q4k1p?usp=drive_link"

# Enlaces a recursos por curso
# Profesor: Herbert Galeano
COURSE_RESOURCES = {
    'matematicas_basicas': "https://drive.google.com/drive/folders/1650yAVCLmN7zDJTITp_kZRD2n63Q4k1p?usp=drive_link",
    'algebra_elemental': "https://drive.google.com/drive/folders/1650yAVCLmN7zDJTITp_kZRD2n63Q4k1p?usp=drive_link",
    'estadistica_descriptiva': "https://drive.google.com/drive/folders/1650yAVCLmN7zDJTITp_kZRD2n63Q4k1p?usp=drive_link",
}

# Mantener compatibilidad
VARK_RESOURCES = COURSE_RESOURCES

# Carpeta de rutas de aprendizaje
LEARNING_PATHS_FOLDER = "https://drive.google.com/drive/folders/1650yAVCLmN7zDJTITp_kZRD2n63Q4k1p?usp=drive_link"

# Configuración detallada de cada curso (Profesor: Herbert Galeano)
LEARNING_MATERIALS = {
    'matematicas_basicas': {
        'name': 'Matemáticas Básicas',
        'code': 'MATH101',
        'icon': 'fa-calculator',
        'color': '#3b82f6',
        'drive_folder': COURSE_RESOURCES['matematicas_basicas'],
        'units': {
            'unidad_1': {
                'name': 'Unidad 1 - Números Naturales',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Números naturales, operaciones básicas, propiedades'
            },
            'unidad_2': {
                'name': 'Unidad 2 - Números Enteros',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Números enteros, operaciones con enteros, recta numérica'
            },
            'unidad_3': {
                'name': 'Unidad 3 - Fracciones',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Fracciones, operaciones con fracciones, simplificación'
            },
            'unidad_4': {
                'name': 'Unidad 4 - Números Decimales',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Decimales, conversiones, operaciones con decimales'
            },
            'unidad_5': {
                'name': 'Unidad 5 - Porcentajes',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Porcentajes, regla de tres, aplicaciones'
            },
            'unidad_6': {
                'name': 'Unidad 6 - Ecuaciones Lineales',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Ecuaciones de primer grado, despeje de variables'
            },
            'unidad_7': {
                'name': 'Unidad 7 - Geometría Básica',
                'url': COURSE_RESOURCES['matematicas_basicas'],
                'description': 'Figuras geométricas, perímetro, área, volumen'
            }
        }
    },
    'algebra_elemental': {
        'name': 'Álgebra Elemental',
        'code': 'ALGE101',
        'icon': 'fa-square-root-alt',
        'color': '#10b981',
        'drive_folder': COURSE_RESOURCES['algebra_elemental'],
        'units': {
            'unidad_1': {
                'name': 'Unidad 1 - Ecuaciones Lineales',
                'url': COURSE_RESOURCES['algebra_elemental'],
                'description': 'Ecuaciones de primer grado, sistemas de ecuaciones'
            },
            'unidad_2': {
                'name': 'Unidad 2 - Gráficas',
                'url': COURSE_RESOURCES['algebra_elemental'],
                'description': 'Representación gráfica de funciones lineales'
            }
        }
    },
    'estadistica_descriptiva': {
        'name': 'Estadística Descriptiva',
        'code': 'STAT101',
        'icon': 'fa-chart-bar',
        'color': '#f59e0b',
        'drive_folder': COURSE_RESOURCES['estadistica_descriptiva'],
        'units': {
            'unidad_1': {
                'name': 'Unidad 1 - Recolección de Datos',
                'url': COURSE_RESOURCES['estadistica_descriptiva'],
                'description': 'Métodos de recolección y organización de datos'
            },
            'unidad_2': {
                'name': 'Unidad 2 - Gráficos Estadísticos',
                'url': COURSE_RESOURCES['estadistica_descriptiva'],
                'description': 'Histogramas, gráficos de barras, circulares'
            },
            'unidad_3': {
                'name': 'Unidad 3 - Medidas de Tendencia Central',
                'url': COURSE_RESOURCES['estadistica_descriptiva'],
                'description': 'Media, mediana, moda y medidas de dispersión'
            }
        }
    }
}

def get_course_materials(course_name_or_id):
    """
    Obtener los materiales de un curso
    
    Args:
        course_name_or_id: Nombre o ID del curso
        
    Returns:
        dict: Diccionario con las unidades y sus enlaces
    """
    # Normalizar nombre del curso
    course_key = course_name_or_id.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e')
    
    # Buscar en el diccionario
    for key, course_data in LEARNING_MATERIALS.items():
        if key in course_key or course_key in key:
            return course_data
    
    # Si es Matemática Básica, retornar por defecto
    if 'matematica' in course_key or 'math' in course_key:
        return LEARNING_MATERIALS['matematica_basica_1']
    
    return None

def get_unit_url(course_name_or_id, unit_number):
    """
    Obtener URL de una unidad específica
    
    Args:
        course_name_or_id: Nombre o ID del curso
        unit_number: Número de unidad (1-7)
        
    Returns:
        str: URL de la unidad o None
    """
    materials = get_course_materials(course_name_or_id)
    
    if not materials:
        return MATH_DRIVE_FOLDER  # Por defecto, carpeta principal
    
    unit_key = f'unidad_{unit_number}'
    
    if unit_key in materials['units']:
        return materials['units'][unit_key]['url']
    
    return MATH_DRIVE_FOLDER  # Por defecto, carpeta principal

