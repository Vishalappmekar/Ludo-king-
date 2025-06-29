from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

users = {}
withdraw_requests = []
tournaments = []

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    uid = str(uuid.uuid4())
    users[uid] = {'name': data.get('name'), 'wallet': 50}
    return jsonify({'status': 'success', 'uid': uid})

@app.route('/api/wallet/<uid>', methods=['GET'])
def wallet_balance(uid):
    user = users.get(uid)
    return jsonify({'wallet': user['wallet']}) if user else ('User not found', 404)

@app.route('/api/tournament/join', methods=['POST'])
def join_tournament():
    data = request.json
    uid = data['uid']
    fee = 10
    if users[uid]['wallet'] >= fee:
        users[uid]['wallet'] -= fee
        tournaments.append({'uid': uid, 'status': 'joined'})
        return jsonify({'status': 'joined'})
    return jsonify({'status': 'insufficient balance'})

@app.route('/api/tournament/win', methods=['POST'])
def win_tournament():
    data = request.json
    uid = data['uid']
    prize = data.get('prize', 40)
    users[uid]['wallet'] += prize
    return jsonify({'status': 'prize added', 'new_wallet': users[uid]['wallet']})

@app.route('/api/withdraw', methods=['POST'])
def request_withdraw():
    data = request.json
    uid = data['uid']
    if users[uid]['wallet'] >= 100:
        users[uid]['wallet'] -= 100
        withdraw_requests.append({'uid': uid, 'amount': 100, 'status': 'pending'})
        return jsonify({'status': 'withdrawal requested'})
    return jsonify({'status': 'low balance'})

@app.route('/api/admin/withdraws', methods=['GET'])
def view_withdraws():
    return jsonify({'requests': withdraw_requests})

@app.route('/api/admin/approve', methods=['POST'])
def approve_withdraw():
    data = request.json
    index = data.get('index')
    if 0 <= index < len(withdraw_requests):
        withdraw_requests[index]['status'] = 'paid'
        return jsonify({'status': 'marked as paid'})
    return jsonify({'error': 'invalid index'})

if __name__ == '__main__':
    app.run(debug=True)