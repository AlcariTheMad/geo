from flask import Flask, Response, abort, redirect, render_template, request

import geometry

app = Flask('geometry')

@app.route('/', methods=['GET', 'POST'])
@app.route('/geo/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('index.html', url=request.path)
    elif request.method == 'POST':
        level = int(request.form.get('level'))
        ranks = int(request.form.get('ranks'))
        calc = request.form.get('calc')
        x, m = geometry.cast(level, ranks, calc)
        if not x:
            x = 'failure'
            m = ''
        return render_template('index.html', x=x, m=m)

if __name__ == '__main__':
    app.run(port=5005)