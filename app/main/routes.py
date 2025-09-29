"""
Rutas principales del STI
"""

from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Student, Teacher, Course, DiagnosticExam
from app import db

@bp.route('/')
@bp.route('/index')
def index():
    """Página principal"""
    if current_user.is_authenticated:
        if current_user.user_type.value == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.user_type.value == 'teacher':
            return redirect(url_for('teacher.dashboard'))
    
    return render_template('index.html', title='Sistema de Tutoría Inteligente')

@bp.route('/about')
def about():
    """Página sobre el sistema"""
    return render_template('about.html', title='Acerca del STI')

@bp.route('/features')
def features():
    """Página de características"""
    return render_template('features.html', title='Características del STI')

@bp.route('/contact')
def contact():
    """Página de contacto"""
    return render_template('contact.html', title='Contacto')

@bp.route('/demo')
def demo():
    """Demo del sistema"""
    return render_template('demo.html', title='Demo del STI')

@bp.route('/api/stats')
def api_stats():
    """API para estadísticas generales del sistema"""
    try:
        stats = {
            'total_students': Student.query.count(),
            'total_teachers': Teacher.query.count(),
            'total_courses': Course.query.count(),
            'completed_diagnostics': DiagnosticExam.query.filter_by(is_completed=True).count()
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
