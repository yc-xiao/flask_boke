from flask import Blueprint, render_template

web2 = Blueprint('web2', __name__, template_folder='templates')

@web2.route('/2')
def helloc():
    return render_template('index2.html')

@web2.route('/1')
def helloc1():
    return render_template('index.html')
