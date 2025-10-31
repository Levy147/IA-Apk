"""
Rutas de autenticación
"""

from flask import render_template, request, redirect, url_for, flash, session
import logging
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.models import User, Student, Teacher
from app.models.user import UserType
from app import db
from app.auth.forms import LoginForm, RegistrationForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Iniciar sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                return render_template('auth/login.html', title='Iniciar Sesión', form=form)
            
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            
            # Redirigir según tipo de usuario
            if user.user_type.value == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.user_type.value == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registrar nuevo usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Verificar si el email ya existe
            if User.query.filter_by(email=form.email.data).first():
                flash('El email ya está registrado.', 'error')
                return render_template('auth/register.html', title='Registrarse', form=form)

            # Crear usuario
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                user_type=UserType(form.user_type.data)
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.flush()  # Obtener user.id sin confirmar toda la transacción

            # Crear perfil específico según tipo de usuario
            if form.user_type.data == 'student':
                student = Student(
                    user_id=user.id,
                    student_id=form.student_id.data,
                    grade_level=form.grade_level.data,
                    school=form.school.data
                )
                db.session.add(student)
            elif form.user_type.data == 'teacher':
                teacher = Teacher(
                    user_id=user.id,
                    teacher_id=form.teacher_id.data,
                    department=form.department.data,
                    specialization=form.specialization.data
                )
                db.session.add(teacher)

            db.session.commit()

            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logging.exception("Error registrando usuario")
            flash(f'Error al registrar usuario: {str(e)}', 'error')
            return render_template('auth/register.html', title='Registrarse', form=form)
    elif request.method == 'POST':
        # Mostrar errores de validación si el formulario no es válido
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return render_template('auth/register.html', title='Registrarse', form=form)

@bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile')
@login_required
def profile():
    """Perfil del usuario"""
    return render_template('auth/profile.html', title='Mi Perfil')
