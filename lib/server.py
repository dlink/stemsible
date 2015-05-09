from flask import Flask, jsonify

from vlib import conf

from users import Users, User

HTTP_BAD_REQUEST = 400

app = Flask(__name__)

@app.route('/users')
def getUsers():
    conf_ = conf.getInstance()
    users = Users()
    users.setColumns(['id',
                      'concat_ws(" ", first_name, last_name) as fullname',
                      'created'])
    users.setOrderBy('id')
    results = users.getTable()
    data = {
        'users': [
            {'id'      : r['id'],
             'fullname': r['fullname'],
             'created' : r['created'],
             'uri': 'http://%s/users/%s' % (conf_.baseurl, r['id']),
             }
            for r in results]
        }
    return jsonify(data)

@app.route('/users/<int:id>')
def getUser(id):
    try:
        user = User(id)
    except Exception, e:
        return problem(e)
    return jsonify(User(id).data)

def problem(e):
    response = {'error': str(e)}
    return jsonify(response), HTTP_BAD_REQUEST

if __name__ == '__main__':
    app.debug = True
    app.run()
