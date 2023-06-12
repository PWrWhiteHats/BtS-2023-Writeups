from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import ValidationError
from wtforms.fields import StringField, SubmitField

content_types = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}
extensions = sorted(content_types.keys())


def is_image():
    def _is_image(form, field):
        if not field.data:
            raise ValidationError()
        elif field.data.filename.split(".")[
            -1
        ].lower() not in extensions or field.data.headers.get("Content-Type") not in [
            content_types[e] for e in extensions
        ]:
            raise ValidationError()

    return _is_image


class MFAForm(FlaskForm):
    default_2fa = "JBSWY3DPEHPK3PXP"
    mfa_image_field = FileField("image", validators=[is_image()])
    mfa_text_field = StringField(
        render_kw={
            "class": "form-control-lg",
            "placeholder": default_2fa,
        },
    )
    submit = SubmitField()
