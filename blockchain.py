from flask import Flask#, jsonify, request, render_template








# inicio de flask app
app = Flask(__name__)


@app.route('/')
def index():
    return "home"
    # return render_template('./index.html')


@app.route('/make/transaction')
def make_transaction():
    return "make transaction"
    # return render_template('./make_transaction.html')


@app.route('/view/transactions')
def view_transaction():
    return "view transaction"
    # return render_template('./view_transactions.html')


@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    response = {
    'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
    'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }

  return jsonify(response), 200
app.run(host='localhost')
