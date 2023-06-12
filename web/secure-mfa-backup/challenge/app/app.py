import binascii
from base64 import b32decode, b32encode, b64encode
from datetime import timedelta
from os import getenv, path
from random import randbytes

from flask import Flask, flash, redirect, render_template, request, session
from flask_bootstrap import Bootstrap5
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from PIL import Image
from pyotp import TOTP, parse_uri
from pyzbar import pyzbar
from utils import MFAForm

challenge_path = path.dirname(path.abspath(__file__))

with open(f"{challenge_path}/../flag") as file:
    FLAG = file.read()

app = Flask(__name__)
app.config["SECRET_KEY"] = "31h091!l-0aw~pqmv"
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.permanent_session_lifetime = timedelta(
    seconds=int(getenv("SESSION_DURATION", 40))
)  # Each user will have a session ID set for 40 seconds (same as frequency of bot)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///:memory:"

db = SQLAlchemy(app)

bootstrap = Bootstrap5(app)
app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "spacelab"
csrf = CSRFProtect(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)


class MFA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100))
    name = db.Column(db.String(100), default="Unknown")
    secret = db.Column(db.String(100))
    issuer = db.Column(db.String(100), default="Unknown")
    interval = db.Column(db.Integer)
    from_image = db.Column(db.Boolean)

    def __repr__(self):
        return self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def is_base32(string):
    try:
        decoded_data = b32decode(string, casefold=True)
        encoded_data = b32encode(decoded_data).decode("utf-8")
        return encoded_data == string
    except binascii.Error:
        return False


@app.before_request
def load_session():
    if not "_uid" in session:
        session["_uid"] = b64encode(randbytes(50)).decode()


@app.route("/", methods=["GET"])
def index():
    if request.cookies.get("FLAG") == FLAG:  # Admin opened
        mfa_query = MFA.query.all()
        db.session.query(MFA).delete()  # Clean DB
        db.session.commit()
        titles = [
            ("uid", "Your ID"),
            ("name", "Name"),
            ("secret", "Secret"),
            ("issuer", "Issuer"),
            ("interval", "Interval"),
            ("from_image", "QR"),
        ]
        return render_template(
            "index.html",
            mfa_form=MFAForm(),
            mfa_list=[m.as_dict() for m in mfa_query],
            titles=titles,
        )
    else:  # Regular user opened
        mfa_query = MFA.query.filter_by(uid=session["_uid"]).all()
        titles = [
            ("uid", "Your ID"),
            ("name", "Name"),
            ("secret", "Secret"),
            ("issuer", "Issuer"),
            ("interval", "Interval"),
            ("OTP", "OTP"),
            ("from_image", "QR"),
        ]
        data = [m.as_dict() for m in mfa_query]
        mfa_list = []
        for mfa in data:
            mfa["OTP"] = TOTP(mfa["secret"]).now()
            mfa.pop("id")
            mfa_list.append(mfa)
        return render_template(
            "index.html", mfa_form=MFAForm(), mfa_list=mfa_list, titles=titles
        )


@app.route("/2fa", methods=["POST"])
@limiter.limit(
    "2/second", key_func=lambda: session.get("_uid"), error_message="Slow down"
)
def create_2fa():
    mfa_form = MFAForm()
    mfa_image = request.files.get("mfa_image_field", None)
    mfa_text = request.form.get("mfa_text_field", None)
    if not mfa_image and not mfa_text:  # User tried to send empty request
        flash("You have to send some data!", category="danger")
        return redirect("/")

    generated_from_qr = False

    if mfa_image and mfa_form.validate_on_submit():  # User supplied QR code as an image
        image = Image.open(mfa_form.mfa_image_field.data)
        image = image.convert("L")
        qr_codes = pyzbar.decode(image)
        mfa_text = "".join([qr_code.data.decode("utf-8") for qr_code in qr_codes])
        generated_from_qr = True
    elif mfa_image and not mfa_form.validate_on_submit():
        flash("Wrong data format", category="danger")
        return redirect("/")

    if mfa_text:  # User supplied 2fa data as a string so we don't have to do anything
        pass

    if mfa_text.startswith("otpauth://"):
        totp = parse_uri(mfa_text)
    elif is_base32(mfa_text):
        totp = TOTP(s=mfa_text)
    else:
        flash("Wrong data format", category="danger")
        return redirect("/")
    new_MFA = MFA(
        uid=session["_uid"],
        name=totp.name,
        secret=totp.secret,
        issuer=totp.issuer,
        interval=totp.__dict__.get("interval", -1),  # HOTP has no interval
        from_image=generated_from_qr,
    )
    db.session.add(new_MFA)
    db.session.commit()
    flash("MFA uploaded", category="success")
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(
        debug=bool(getenv("DEBUG", False)),
        port=int(getenv("PORT", 8080)),
        host=getenv("HOST", "127.0.0.1"),
    )
