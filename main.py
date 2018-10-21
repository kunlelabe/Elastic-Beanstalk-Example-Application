# TODO
# Add requirements.txt
# Add Google Analytics
# Add French
	# Idea: if session['FR'], then use lookup table
		# Open to XSS?
	# Will nicely group all EN-FR translations in single file, easy to send to translation people
	# Use gettext and/or Flask-Babel
# Protect against SQL injection and XSS
# Navbar colour in dropdown
# pull / push to display FIPs on iPad
# Always use px vs em?

from flask import Flask, flash, redirect, render_template, request, session, url_for
import my_forms
from highcharts import inst_led

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/departmental')
def departmental():
	return render_template('departmental.html')


@app.route('/instructor-led', methods=['GET', 'POST'])
def instructor_led():
	form = my_forms.CourseForm(request.form)
	if request.method == 'POST' and form.validate():
		course_title = form.course_title.data
		return redirect(url_for('inst_led_dash', course_title=course_title))
	return render_template('form.html', form=form, title="Dashboard Parameters", button_val="Go")


@app.route('/inst-led-dash')
def inst_led_dash():
	# Get arguments from query string
	course_title = request.args['course_title']
	top_5_depts_j = inst_led.top_5_depts(course_title)
	top_5_classifs_j = inst_led.top_5_classifs(course_title)
	return render_template('instructor-led.html', course_title=course_title,
												  top_5_depts_j=top_5_depts_j,
												  top_5_classifs_j=top_5_classifs_j)


@app.route('/online')
def online():
	return render_template('online.html')


if __name__ == '__main__':
	app.run()
