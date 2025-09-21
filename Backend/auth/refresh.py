from . import auth_bp
from app_logging import normal_logs
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies,get_jwt_identity

one_log = normal_logs()

@auth_bp.route("/refresh-tokens",methods=["POST"])
@jwt_required(refresh=True)
def renew_tokens():
    get_id = get_jwt_identity()
    if not get_id:
        one_log.warning("refresh cookies is missing")
        return jsonify({"message":"Refresh token missing.Please log in again."})
    
    check_validity = User.query.filter_by(id=get_id).first()
    if not check_validity:
        one_log.warning("Id in refresh token is not matching any Id in the User table.")
        return jsonify({"message":"Invalid refresh token, please login again."})
    access_token = create_access_token(identity=check_validity.id)
    refresh_token = create_refresh_token(identity=check_validity.id)
    response = jsonify({"message":"Token refreshed successfully"})
    set_access_cookies(response,access_token)
    set_refresh_cookies(response,refresh_token)
    return response
    
    
