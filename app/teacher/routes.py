"""
Rutas para docentes
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.teacher import bp
from app.models import Teacher, Course, Student, DiagnosticExam, LearningPath, Progress
from app import db
from app.teacher.forms import CourseForm, QuestionForm
from sqlalchemy import func
import json

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del docente"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    if not teacher:
        flash('Perfil de docente no encontrado.', 'error')
        return redirect(url_for('auth.logout'))
    
    # Obtener cursos del docente
    courses = teacher.courses
    
    # Estadísticas generales
    total_students = sum(course.get_student_count() for course in courses)
    total_diagnostics = DiagnosticExam.query.join(Course).filter(
        Course.teacher_id == teacher.id
    ).count()
    
    completed_diagnostics = DiagnosticExam.query.join(Course).filter(
        Course.teacher_id == teacher.id,
        DiagnosticExam.is_completed == True
    ).count()
    
    # Progreso promedio de estudiantes
    avg_progress = db.session.query(func.avg(CourseEnrollment.overall_progress)).join(Course).filter(
        Course.teacher_id == teacher.id,
        CourseEnrollment.is_active == True
    ).scalar() or 0
    
    dashboard_data = {
        'teacher': teacher,
        'courses': courses,
        'total_students': total_students,
        'total_diagnostics': total_diagnostics,
        'completed_diagnostics': completed_diagnostics,
        'avg_progress': avg_progress * 100  # Convertir a porcentaje
    }
    
    return render_template('teacher/dashboard.html', title='Dashboard Docente', **dashboard_data)

@bp.route('/courses')
@login_required
def courses():
    """Lista de cursos del docente"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    courses = teacher.courses
    
    return render_template('teacher/courses.html', 
                         title='Mis Cursos', 
                         courses=courses)

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    """Detalle de un curso específico"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    course = Course.query.get_or_404(course_id)
    
    # Verificar que el curso pertenece al docente
    if course.teacher_id != teacher.id:
        flash('Acceso denegado a este curso.', 'error')
        return redirect(url_for('teacher.courses'))
    
    # Obtener estudiantes matriculados
    enrollments = course.enrollments
    students = [e.student for e in enrollments if e.is_active]
    
    # Estadísticas del curso
    total_students = len(students)
    completed_diagnostics = DiagnosticExam.query.filter_by(
        course_id=course_id,
        is_completed=True
    ).count()
    
    # Progreso promedio
    avg_progress = sum(e.overall_progress for e in enrollments if e.is_active) / total_students if total_students > 0 else 0
    
    return render_template('teacher/course_detail.html',
                         title=f'Curso: {course.name}',
                         course=course,
                         students=students,
                         total_students=total_students,
                         completed_diagnostics=completed_diagnostics,
                         avg_progress=avg_progress * 100)

@bp.route('/course/<int:course_id>/students')
@login_required
def course_students(course_id):
    """Lista de estudiantes de un curso"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    course = Course.query.get_or_404(course_id)
    
    # Verificar que el curso pertenece al docente
    if course.teacher_id != teacher.id:
        flash('Acceso denegado a este curso.', 'error')
        return redirect(url_for('teacher.courses'))
    
    # Obtener estudiantes con información detallada
    enrollments = course.enrollments
    students_data = []
    
    for enrollment in enrollments:
        if enrollment.is_active:
            student = enrollment.student
            diagnostic = DiagnosticExam.query.filter_by(
                course_id=course_id,
                student_id=student.id
            ).first()
            
            learning_path = LearningPath.query.filter_by(
                course_id=course_id,
                student_id=student.id,
                is_active=True
            ).first()
            
            students_data.append({
                'student': student,
                'enrollment': enrollment,
                'diagnostic': diagnostic,
                'learning_path': learning_path,
                'vark_profile': student.get_vark_profile() if student.diagnostic_completed else None
            })
    
    return render_template('teacher/course_students.html',
                         title=f'Estudiantes - {course.name}',
                         course=course,
                         students_data=students_data)

@bp.route('/student/<int:student_id>/progress')
@login_required
def student_progress(student_id):
    """Progreso detallado de un estudiante"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    student = Student.query.get_or_404(student_id)
    
    # Verificar que el docente tiene acceso a este estudiante
    student_courses = [e.course for e in student.enrollments if e.course.teacher_id == teacher.id]
    if not student_courses:
        flash('No tienes acceso a este estudiante.', 'error')
        return redirect(url_for('teacher.dashboard'))
    
    # Obtener progreso del estudiante
    progress_records = Progress.query.filter_by(student_id=student_id).all()
    
    # Obtener rutas de aprendizaje
    learning_paths = LearningPath.query.filter_by(student_id=student_id).all()
    
    return render_template('teacher/student_progress.html',
                         title=f'Progreso de {student.user.get_full_name()}',
                         student=student,
                         student_courses=student_courses,
                         progress_records=progress_records,
                         learning_paths=learning_paths)

@bp.route('/analytics')
@login_required
def analytics():
    """Analíticas y reportes"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    courses = teacher.courses
    
    # Datos para gráficos
    analytics_data = {
        'courses': [],
        'student_progress': [],
        'learning_styles': {'V': 0, 'A': 0, 'R': 0, 'K': 0},
        'diagnostic_completion': 0
    }
    
    for course in courses:
        enrollments = course.enrollments
        active_enrollments = [e for e in enrollments if e.is_active]
        
        if active_enrollments:
            avg_progress = sum(e.overall_progress for e in active_enrollments) / len(active_enrollments)
            analytics_data['courses'].append({
                'name': course.name,
                'students': len(active_enrollments),
                'avg_progress': avg_progress * 100
            })
            
            # Contar estilos de aprendizaje
            for enrollment in active_enrollments:
                student = enrollment.student
                if student.dominant_learning_style:
                    analytics_data['learning_styles'][student.dominant_learning_style] += 1
            
            # Contar diagnósticos completados
            completed = DiagnosticExam.query.filter_by(
                course_id=course.id,
                is_completed=True
            ).count()
            analytics_data['diagnostic_completion'] += completed
    
    return render_template('teacher/analytics.html',
                         title='Analíticas',
                         analytics_data=analytics_data)

@bp.route('/create-course', methods=['GET', 'POST'])
@login_required
def create_course():
    """Crear nuevo curso"""
    if current_user.user_type.value != 'teacher':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.index'))
    
    teacher = current_user.teacher_profile
    form = CourseForm()
    
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            description=form.description.data,
            code=form.code.data,
            teacher_id=teacher.id,
            grade_level=form.grade_level.data,
            subject=form.subject.data,
            credits=form.credits.data,
            diagnostic_required=form.diagnostic_required.data,
            min_diagnostic_questions=form.min_diagnostic_questions.data
        )
        
        db.session.add(course)
        db.session.commit()
        
        flash('¡Curso creado exitosamente!', 'success')
        return redirect(url_for('teacher.course_detail', course_id=course.id))
    
    return render_template('teacher/create_course.html',
                         title='Crear Curso',
                         form=form)

@bp.route('/api/course/<int:course_id>/stats')
@login_required
def api_course_stats(course_id):
    """API para estadísticas de un curso"""
    if current_user.user_type.value != 'teacher':
        return jsonify({'error': 'Acceso denegado'}), 403
    
    teacher = current_user.teacher_profile
    course = Course.query.get_or_404(course_id)
    
    # Verificar que el curso pertenece al docente
    if course.teacher_id != teacher.id:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    # Obtener estadísticas
    enrollments = course.enrollments
    active_enrollments = [e for e in enrollments if e.is_active]
    
    stats = {
        'total_students': len(active_enrollments),
        'completed_diagnostics': DiagnosticExam.query.filter_by(
            course_id=course_id,
            is_completed=True
        ).count(),
        'avg_progress': sum(e.overall_progress for e in active_enrollments) / len(active_enrollments) * 100 if active_enrollments else 0,
        'learning_paths_created': LearningPath.query.filter_by(course_id=course_id).count()
    }
    
    return jsonify(stats)
