from datetime import timedelta, datetime, date

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from wtforms.validators import DataRequired
import os


images = UploadSet('images', IMAGES,default_dest=lambda app: os.path.join(app.instance_path,"uploads"))


class DriverRegistrationForm(FlaskForm):
    firstname = StringField('First Name', [validators.Length(min=2, max=40),DataRequired()])
    lastname = StringField('Last Name', [validators.Length(min=2, max=40),DataRequired()])
    license_plate_num = StringField('License Plate Number', [validators.Length(min=7, max=7),DataRequired()],render_kw={'maxlength': '7'})
    contact_num = StringField('Phone Number', [validators.Length(min=7, max=7), DataRequired()],
                         render_kw={'maxlength': '7'})
    veh_color = StringField('Vehicle Color', [validators.Length(min=2, max=40), DataRequired()])
    veh_brand = StringField('Vehicle Brand', [validators.Length(min=2, max=40), DataRequired()])
    veh_make = StringField('Vehicle Make', [validators.Length(min=2, max=40), DataRequired()])
    id_picture = FileField('ID Picture', [FileRequired(), FileAllowed(images, 'Images only!')])


