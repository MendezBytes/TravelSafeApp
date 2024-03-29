import glob
import logging
import os
import traceback
import uuid
from datetime import datetime
from shutil import copyfile
from pathlib import Path
import qrcode
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_uploads import configure_uploads
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from config import BaseConfig
from forms.signup_page_forms import DriverRegistrationForm, id_images,car_images
from init_scripts.db_init import init_db
from models.db_models import Base, Drivers
from utility_functions.encrypter import encode_license_num, decode_license_num
from utility_functions.utility_methods import current_milli_time

app = Flask(__name__)
init_db()
app.config.from_object(BaseConfig)

cors = CORS()
cors.init_app(app)

configure_uploads(app, [id_images,car_images])
#Make sure directories are present
Path(os.path.join(app.instance_path,"uploads/id_pics")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(app.instance_path,"uploads/car_pics")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(app.static_folder,"generated_qr_code")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(app.static_folder,"temp_images")).mkdir(parents=True, exist_ok=True)

try:
    engine = create_engine(app.config.get('DATABASE_URI'), convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
except Exception as e:
    print(traceback.format_exc())


@app.route('/', methods=['GET', 'POST'])
def driver_register_page():
    try:
        form = DriverRegistrationForm(CombinedMultiDict((request.files, request.form)))
        if request.method == "POST" and form.validate_on_submit():
            # TODO Check if driver exists using license plate, return their current info by verifying other fields
            driver = db_session.query(Drivers).filter(
                func.upper(Drivers.license_plate) == form.license_plate_num.data.upper()).first()
            if driver:
                # TODO Add a error string saying driver exists
                return render_template('driver_signup_page.html', form=DriverRegistrationForm())
            # Save images
            id_pic_filename = id_images.save(request.files['id_picture'], name=form.license_plate_num.data.upper() + ".")
            car_pic_filename = car_images.save(request.files['car_picture'], name=form.license_plate_num.data.upper() + ".")
            # TODO possiblt validate license plate here?
            # TODO also possibly validate id card num

            new_driver = Drivers(driver_uuid=str(uuid.uuid1()), firstname=form.firstname.data,
                                 lastname=form.lastname.data, license_plate=form.license_plate_num.data.upper(),
                                 contact_num=form.contact_num.data, vehicle_color=form.veh_color.data,
                                 vehicle_brand=form.veh_brand.data, vehicle_make=form.veh_make.data,
                                 added_date=datetime.now(), ip_address=request.remote_addr,
                                 id_picture_path=id_pic_filename,car_pic_path=car_pic_filename, user_agent=request.user_agent.string)
            db_session.add(new_driver)
            db_session.commit()
            qr_code_data = request.base_url + "driverCheck/" + encode_license_num(new_driver.driver_id,
                                                                                  new_driver.license_plate)
            new_driver.qr_data = qr_code_data
            db_session.commit()
            # Generate qr code
            img = qrcode.make(qr_code_data)
            qr_code_image_name = str(current_milli_time()) +"qr_code.png"
            qr_code_path = os.path.join(app.static_folder, "generated_qr_code",qr_code_image_name)
            #Clear the contents of the folder
            files = glob.glob(os.path.join(app.static_folder, "generated_qr_code","*"))
            for f in files:
                os.remove(f)
            qr_code_url = app.static_url_path + "/generated_qr_code/" + qr_code_image_name
            img.save(qr_code_path)

            return render_template('qr_code_success.html', qrcode=qr_code_url)
        return render_template('driver_signup_page.html', form=DriverRegistrationForm())
    except Exception as e:
        print(traceback.format_exc())
        return traceback.format_exc()
        #return render_template('driver_signup_page.html', form=DriverRegistrationForm())


@app.route('/driverCheck/<encrypted_string>')
def driverCheck(encrypted_string):
    try:
        driver_id, license_plate = decode_license_num(encrypted_string)
        driver = db_session.query(Drivers).filter(Drivers.driver_id == int(driver_id)).first()
        driver_pic = os.path.join(app.instance_path, "uploads", driver.id_picture_path)
        car_pic = os.path.join(app.instance_path, "uploads", driver.car_pic_path)
        if driver and os.path.exists(driver_pic):
            #Temporarily move over image to static
            #Delete existing files
            files = glob.glob(os.path.join(app.static_folder, "temp_images", "*"))
            for f in files:
                os.remove(f)
            temp_car_pic = str(current_milli_time()) + "car_temp.png"
            temp_driver_pic = str(current_milli_time()) + "id_temp.png"
            copyfile(car_pic,  os.path.join(app.static_folder, "temp_images",temp_car_pic))
            copyfile(driver_pic,  os.path.join(app.static_folder, "temp_images",temp_driver_pic))
            driver_url = app.static_url_path + "/temp_images/" + temp_driver_pic
            car_url = app.static_url_path + "/temp_images/" + temp_car_pic
            return render_template('driverInfoPage.html', driver=driver, driver_pic=driver_url ,car_pic = car_url)
        else:
            return "No driver found"
    except Exception as e:
        print(traceback.format_exc())
        return "An Error has occurred"


@app.route('/qrscan', methods=['GET', 'POST'])
def qr_scan():
    return render_template('qr_scan.html')


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run()
