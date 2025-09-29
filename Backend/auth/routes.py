from flask import jsonify,request,url_for,current_app
import secrets
import traceback
from datetime import datetime,timedelta
print(">>> loading auth/routes.py")
from . import other_routes
from . import auth_bp
from models import User,ResetToken,SessionStorage,db
from app_logging import normal_logs
from tasks import send_emails
from flask_jwt_extended import create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,unset_jwt_cookies,decode_token


my_log = normal_logs()

@auth_bp.route("/register", methods=["POST"])
def sign_up():
    print(">>> Incoming request:", request.method)  
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error":"Invalid JSON"})
    name = data.get("name",None)
    email = data.get("email",None)
    password = data.get("password",None)
    
    if not all([name,email,password]):
        return jsonify({"message":"Please fill all inputs"})
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"status":"e","message":"User already exist please sign in."})
    try:
        print(">>> Creating new user:", name, email)
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
        link = url_for("auth.verify_email",token=token,_external=True)
        body = f"Please click on the link to verify your email.\n\n{link}"
        status = send_emails(new_user.email,subject,body)
        if status is None:
            return jsonify({"status":"error","message":"Error occurred when sending email, please request for another verification email"})
        elif status == "600":
            return jsonify({"status":"error","message":"Oops email never get sent, please tryagain another time."})
        else:
            return jsonify({"status":"s","message":"User created successfully, we've sent a verification email, please check your inbox"})
    except Exception as e:
        traceback.print_exc()
        print(">>> Exception occurred:", e)
        my_log.error(f"Error:{e}")
        db.session.rollback()
        return jsonify({"status":"e" ,"message":"Please an error occurred during sign up,can try again later"})

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
                access_token = create_access_token(identity=str(existence.id))
                refresh_token = create_refresh_token(identity=str(existence.id))
                response = jsonify({"message":"User logged in successfully","user":existence.to_dic() ,"status":"s" })
                set_access_cookies(response,access_token)
                set_refresh_cookies(response,refresh_token)
                return response
            else:
                return jsonify({"message":"Password is invalid" , "status":"e"})
        else:
            try:
                raw_token = secrets.token_urlsafe(32)
                storing = SessionStorage(user_id=existence.id)
                storing.set_hash(raw_token)
                db.session.add(storing)
                db.session.commit() 
                return jsonify({"status":"e","message":"Email not verified. Please verify your account.","resend_verification_url":url_for("auth.resend_verification",token=raw_token,_external=True)})
            except Exception as e:
                db.session.rollback()
                my_log.error(f"Error: {e}")
                return jsonify({"message":"Oops something went wrong when trying to login."})    
    else:   
        return jsonify({"message":"Please sign up first."})
    
@auth_bp.route("/logout",methods=["POST"])
def close():
    response = jsonify({"message":"User logged out successfully"})
    unset_jwt_cookies(response)
    return response                          



