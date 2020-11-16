from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/js_test')
def get_index():
    return '<html><center><script>document.write("Hello, i`am js!")</script></center></html>'


if __name__ == '__main__':
    app.run()
