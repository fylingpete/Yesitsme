from flask import Flask, render_template, request, session
import pyotp
import qrcode
from flask import send_from_directory



app = Flask(__name__)
app.secret_key = 'xsdfsdfw2323'  # Replace with a strong secret key

@app.route('/')
def setup():
    secret = pyotp.random_base32()  # Generate new shared secret
    session['secret'] = secret

    # Generate QR code
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name='user@totp-authenticator', issuer_name='TOTP Authenticator')
    img = qrcode.make(uri)
    img.save('templates/qr_code.png')

    return render_template('setup.html', secret=secret, qr_code='qr_code.png')

@app.route('/generate')
def generate_code():
    secret = session.get('secret')
    if not secret:
        return 'Please complete setup first' 

    totp = pyotp.TOTP(secret)
    current_code = totp.now()
    return render_template('generate.html', code=current_code)

@app.route('/verify', methods=['POST'])
def verify_code():
    secret = session.get('secret')
    user_code = request.form['code']

    totp = pyotp.TOTP(secret)
    if totp.verify(user_code):
        return 'Code verification successful!'
    else:
        return 'Invalid code, please try again.'
    
@app.route('/templates/<filename>')
def send_file(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    app.run(debug=True) 
