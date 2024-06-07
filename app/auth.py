from flask import Blueprint, render_template, request, flash, redirect, url_for

auth = Blueprint('auth',__name__)

ADMIN = {'username':'admin', 'Password':'0000'}
 
@auth.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']

        if username != ADMIN['username'] or password != ADMIN['Password']:
            flash('wrong username or password', category='error')
        else:
            return redirect(url_for('views.formation'))
    return render_template('admin.html')