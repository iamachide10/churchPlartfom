from . import auth_bp
from app_logging import normal_logs
from flask import jsonify,request
import secrets
from tasks import send_emails
from models import User,ResetToken,SessionStorage,db
from datetime import datetime,timedelta

mine_log = normal_logs()


@auth_bp.route("/resend-verification",methods=["POST"])
def verification_resend():
    get_token = request.args.get("token")
    if not get_token:
        return jsonify({"message":"Couldn't retrieve token"})
    check_existence = None
    verify = SessionStorage.query.all()
    for each in verify:
        if each.check_hash(get_token):
            check_existence = each 
            break
    if check_existence is None:
        mine_log.warning("Warning, user token was unidentified in the database")
        return jsonify({"message":"Couldn't identify user."})

    verify = User.query.filter_by(id=check_existence.user_id).first()
    if not verify:
        return jsonify({"message":"Couldn't identify user."})
    if verify.is_verified:
        return jsonify({"message":"Please this account is already verified"})
    try:
        token = secrets.token_urlsafe(32)
        expiration = datetime.utcnow() + timedelta(minutes=15)
        reset_token = ResetToken(user_id=verify.id,token=token,expires_at=expiration)
        db.session.delete(check_existence)
        db.session.add(reset_token)
        db.session.commit()
        subject = "Please verify your account."
        link = url_for("verify_email",token=token,_external=True)
        body = f"Please verify your account by clicking on this link below.\n\n\t{link}"
        status = send_emails.(verify.email,subject,body)
        if status is None:
            return jsonify({"status":"error","message":"Error occurred when sending email, please request for another verification email link"})
        elif status == "600":
            return jsonify({"status":"error","message":"Oops email never get sent, please tryagain another time."})
        else:
            return jsonify({"status":"s","message":"Verification email sent successfully,please check your inbox"})
    except Exception as e:
        db.session.rollback()
        mine_log.error(f"Error: {e}")
        return jsonify({"message":"Something went wrong whiles trying to resend verification email."})

@auth_bp.route("/verification-email",methods=["GET"])
def verify_email():
    get_token = request.args.get("token")
    if not get_token:
        return jsonify({"status":"error","message":"Absence of token"})
    verify = ResetToken.query.filter_by(token=get_token).first()
    if not verify:
        return jsonify({"message":"Token is invalid"})
    check_match = User.query.filter_by(id=verify.user_id).first()
    if not check_match:
        mine_log.warning("Userid in ResetToken class is not matching the id in User class")
        return jsonify({"message":"Couldn't identify user trying to verify email."})
    if check_match.is_verified:
        return jsonify({"message":"Please this account is already verified."})
    if datetime.utcnow() > verify.expires_at:
        return jsonify({"message":"Token has expired,Please request for another verification email."})
    try:
        check_match.is_verified = True
        db.session.delete(verify)
        db.seesion.commit()
        return jsonify({"status":"success","message":"User account was successfully verified"})
    except Exception as e:
        db.session.rollback()
        mine_log.error(f"Error occurred with {verify.user_id}: {e}")
        return jsonify({"status":"failed","message":"Oops an error occurred during verification."})
    
@auth_bp.route("/reset-password-request",methods=["POST"])
def reset_password():
    data = get_json(silent=True)
    if not data:
        return jsonify({"error":"Invalid JSON"})
    email = data.get("email")
    if not email:
        return jsonify({"message":"Email is required"})
    check_validity = User.query.filter_by(email=email).first()
    if not check_validity:
        return jsonify({"message":"If an account with this email exists, you will receive a password reset email shortly."})
    try:
        token = secrets.token_urlsafe(32)
        expiration = datetime.utcnow() + timedelta(minutes=15)
        reset_token = ResetToken(user_id=check_validity.id,token=token,expires_at=expiration)
        db.session.add(reset_token)
        db.session.commit()
        subject = "Reset Your Password"
        link = url_for("password_reset",token=token,_external=True)
        body = f"Click on this link to reset your password.\n\n{link}"
        status = send_emails.(check_validity.email,subject,body)
        if status is None:
            return jsonify({"status":"error","message":"Error occurred when sending reset password link, please request for another link."})
        elif status == "600":
            return jsonify({"status":"error","message":"Oops password link never get sent, please tryagain another time."})
        else:
            return jsonify({"status":"s","message":"Reset password link has been sent successfully,please check your inbox"})
    except Exception as e:
        db.session.rollback()
        mine_log.error(f"Error occurred with {check_validity.id}: {e}")
        return jsonify({"status":"error","message":"Error occurred when trying to send password reset link,try again later or request another reset link."})


@auth_bp.route("/reset-password",methods=["POST"])
def password_reset():
    retrieve_token = request.args.get("token")
    if not retrieve_token:
        return jsonify({"message":"Token is missing."})
    check_validity = ResetToken.query.filter_by(token=retrieve_token).first()
    if not check_validity:
        return jsonify({"message":"Invalid or expired token"})
    check_match = User.query.filter_by(id=check_validity.user_id).first()
    if not check_match:
        mine_log.warning("User id in ResetToken is not matching User class table")
        return jsonify({"status":"error","message":"Couldn't identify user trying to make password reset"})
    if datetime.utcnow() > check_validity.expires_at:
        return jsonify({"message":"Token has expired already"})
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message":"Invalid JSON"})
    new_password = data.get("password")
    if not new_password:
        return jsonify({"message":"Please you must include new password"})
    try:
        check_match.hash_password(new_password)
        db.session.delete(check_validity)
        db.session.commit()
        return jsonify({"status":"success","message":"Password has been reset successfully"})
    except Exception as e:
        db.session.rollback()
        mine_log.error(f"An error occurred with {check_match.id}, when password reset was going on: {e}")
        return jsonify({"status":"error","message":"An error occurred when password reset was going on."})
    
    



