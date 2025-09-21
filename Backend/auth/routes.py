from flask import jsonify,request,url_for,current_app
import secrets
from datetime import datetime,timedelta
print(">>> loading auth/routes.py")
from . import auth_bp
from models import User,ResetToken,SessionStorage,db
from app_logging import normal_logs
from utils import send_emails
from flask_jwt_extended import create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,unset_jwt_cookies,decode_token


my_log = normal_logs()

@auth_bp.route("/register",methods=["POST"])
def sign_up():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error":"Invalid JSON"})
    name = data.get("userName",None)
    email = data.get("email",None)
    password = data.get("password",None)
    
    if not all([name,email,password]):
        return jsonify({"message":"Please fill all inputs"})
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message":"There was an issue with your sign-up.Please try again"})
    try:
        new_user = User(user_name = name, email = email)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.flush()
        token = secrets.token_urlsafe(32)
        expiration_time = datetime.utcnow() + timedelta(minutes=15)
        reset_token = ResetToken(user_id=new_user.id,token=token,expires_at=expiration_time)
        db.session.add(reset_token) 
        db.session.commit()
        subject = "Please verify your email"
        link = url_for("verify_email",token=token,_external=True)
        body = f"Please click on the link to verify your email.\n\n{link}"
        task = send_emails.delay(new_user.email,subject,body)

        return jsonify({"success":"User registered successfully","message":"we've sent a verification email, please check your inbox","user":new_user.to_dic()})
    except Exception as e:
        my_log.error(f"Error:{e}")
        db.session.rollback()
        return jsonify({"message":"Please an error occurred during sign up,can tryagain later"})

print(">>> finished loading auth/routes.py")

@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error":"Invalid JSON"})
    email = data.get("email",None)
    password = data.get("password",None)

    if not all([email,password]):
        return jsonify({"message":"Please login requires email and password"})
    
    existence = User.query.filter_by(email=email).first()
    if existence:
        if existence.is_verified:
            if existence.verify_password(password):
                access_token = create_access_token(identity=existence.id)
                refresh_token = create_refresh_token(identity=existence.id)
                response = jsonify({"message":"User logged in successfully","user":existence.to_dic()})
                set_access_cookies(response,access_token)
                set_refresh_cookies(response,refresh_token)
                return response
            else:
                return jsonify({"message":"Password is invalid"})
        else:
            try:
                raw_token = secrets.token_urlsafe(32)
                storing = SessionStorage(user_id=existence.id)
                storing.set_hash(raw_token)
                db.session.add(storing)
                db.session.commit() 
                return jsonify({"issue":"verification","message":"Email not verified. Please verify your account.","resend_verification_url":url_for("resend_verification",token=raw_token,_external=True)})
            except Exception as e:
                db.session.rollback()
                my_log.error(f"Error: {e}")
                return jsonify({"message":"Oops something went wrong when trying to login."})    
    else:   
        return jsonify({"message":"Please sign in first."})
    
@auth_bp.route("/logout",methods=["POST"])
def close():
    response = jsonify({"message":"User logged out successfully"})
    unset_jwt_cookies(response)
    return response                      
    