"""
Modelos de usuarios para el STI
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum
from app import db

class UserType(enum.Enum):
    """Tipos de usuario en el sistema"""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class User(UserMixin, db.Model):
    """Modelo base de usuario"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relaciones
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    teacher_profile = db.relationship('Teacher', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Obtener nombre completo"""
        return f"{self.first_name} {self.last_name}"
    
    def update_last_login(self):
        """Actualizar último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()

class Student(db.Model):
    """Perfil de estudiante"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # Carnet
    grade_level = db.Column(db.String(20))  # Nivel educativo
    school = db.Column(db.String(100))
    
    # Información de estilo de aprendizaje VARK
    vark_visual = db.Column(db.Float, default=0.0)
    vark_auditory = db.Column(db.Float, default=0.0)
    vark_reading = db.Column(db.Float, default=0.0)
    vark_kinesthetic = db.Column(db.Float, default=0.0)
    dominant_learning_style = db.Column(db.String(20))  # V, A, R, K
    
    # Estado del diagnóstico
    diagnostic_completed = db.Column(db.Boolean, default=False)
    diagnostic_score = db.Column(db.Float)
    diagnostic_date = db.Column(db.DateTime)
    
    # Estado de la ruta de aprendizaje
    learning_path_created = db.Column(db.Boolean, default=False)
    current_step = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    enrollments = db.relationship('CourseEnrollment', backref='student', cascade='all, delete-orphan', lazy='dynamic')
    exam_responses = db.relationship('ExamResponse', backref='student', cascade='all, delete-orphan', lazy='dynamic')
    vark_responses = db.relationship('VARKResponse', backref='student', cascade='all, delete-orphan', lazy='dynamic')
    learning_paths = db.relationship('LearningPath', backref='student', cascade='all, delete-orphan', lazy='dynamic')
    progress_records = db.relationship('Progress', backref='student', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<Student {self.student_id}>'
    
    def get_vark_profile(self):
        """Obtener perfil VARK del estudiante"""
        return {
            'visual': self.vark_visual,
            'auditory': self.vark_auditory,
            'reading': self.vark_reading,
            'kinesthetic': self.vark_kinesthetic,
            'dominant': self.dominant_learning_style
        }
    
    def update_vark_profile(self, visual, auditory, reading, kinesthetic):
        """Actualizar perfil VARK"""
        self.vark_visual = visual
        self.vark_auditory = auditory
        self.vark_reading = reading
        self.vark_kinesthetic = kinesthetic
        
        # Determinar estilo dominante
        scores = {
            'V': visual,
            'A': auditory,
            'R': reading,
            'K': kinesthetic
        }
        self.dominant_learning_style = max(scores, key=scores.get)
        db.session.commit()

class Teacher(db.Model):
    """Perfil de docente"""
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False)  # Código de docente
    department = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    years_experience = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    courses = db.relationship('Course', backref='teacher', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Teacher {self.teacher_id}>'
