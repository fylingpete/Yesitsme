from flask import Flask, render_template, request, redirect, url_for
import pyotp
import qrcode
import os

app = Flask(__name__)


@app.route('/')
def setup():
    secret = request.args.get('secret')
    print("Setup route called with secret:", secret)
    if secret:
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(
            name='user@yesitsme', issuer_name='Yesitsme')
        img = qrcode.make(uri)
        img.save('static/qr_code.png')

        # # Assuming 'qr_code.png' is in the 'templates' folder
        # current_path = os.path.join('templates', 'qr_code.png')
        # new_path = os.path.join('qr_code.png')

        # # Move the file
        # os.rename(current_path, new_path)

        return render_template('setup.html', secret=secret, qr_code='qr_code.png')

    else:
        return redirect(url_for('shared_key'))


@app.route('/generate')
def generate_code():
    secret = request.args.get('secret')
    if not secret:
        return 'Missing shared secret. Please start at the setup page.'

    totp = pyotp.TOTP(secret)
    current_code = totp.now()
    return render_template('generate.html', code=current_code)


@app.route('/verify', methods=['POST'])
def verify_code():
    secret = request.args.get('secret')
    user_code = request.form['code']

    totp = pyotp.TOTP(secret)
    if totp.verify(user_code):
        return 'Code verification successful!'
    else:
        return 'Invalid code, please try again.'


@app.route('/shared_key', methods=['GET', 'POST'])
def shared_key():
    if request.method == 'POST':
        shared_key = request.form['key']
        return redirect(url_for('setup', secret=shared_key))
    else:
        return render_template('shared_key.html')


if __name__ == '__main__':
    app.run(debug=True)
