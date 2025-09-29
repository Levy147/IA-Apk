"""
Modelos de cursos y matrículas
"""

from datetime import datetime
import enum
from app import db

class CourseStatus(enum.Enum):
    """Estados de un curso"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Course(db.Model):
    """Modelo de curso"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(20), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    
    # Configuración del curso
    grade_level = db.Column(db.String(20))  # Nivel educativo
    subject = db.Column(db.String(50))  # Materia
    credits = db.Column(db.Integer, default=1)
    
    # Estado y fechas
    status = db.Column(db.Enum(CourseStatus), default=CourseStatus.ACTIVE)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Configuración de evaluación
    diagnostic_required = db.Column(db.Boolean, default=True)
    min_diagnostic_questions = db.Column(db.Integer, default=25)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    enrollments = db.relationship('CourseEnrollment', backref='course', cascade='all, delete-orphan')
    competencies = db.relationship('Competency', backref='course', cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='course', cascade='all, delete-orphan')
    resources = db.relationship('Resource', backref='course', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'
    
    def get_enrolled_students(self):
        """Obtener estudiantes matriculados"""
        return [enrollment.student for enrollment in self.enrollments if enrollment.is_active]
    
    def get_student_count(self):
        """Obtener número de estudiantes matriculados"""
        return len([e for e in self.enrollments if e.is_active])

class CourseEnrollment(db.Model):
    """Matrícula de estudiante en curso"""
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Estado de la matrícula
    is_active = db.Column(db.Boolean, default=True)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    
    # Progreso del estudiante en el curso
    overall_progress = db.Column(db.Float, default=0.0)  # 0.0 a 1.0
    current_competency = db.Column(db.String(100))
    
    # Calificaciones
    final_grade = db.Column(db.Float)
    diagnostic_grade = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    learning_paths = db.relationship('LearningPath', backref='enrollment', cascade='all, delete-orphan')
    progress_records = db.relationship('Progress', backref='enrollment', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Enrollment {self.student.student_id} in {self.course.code}>'
    
    def update_progress(self, progress_value):
        """Actualizar progreso del estudiante"""
        self.overall_progress = min(1.0, max(0.0, progress_value))
        db.session.commit()
    
    def complete_course(self):
        """Marcar curso como completado"""
        self.completion_date = datetime.utcnow()
        self.overall_progress = 1.0
        self.is_active = False
        db.session.commit()
