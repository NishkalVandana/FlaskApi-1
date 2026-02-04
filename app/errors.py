from flask import jsonify
from app.exceptions import APIException

def register_error_handlers(app):

    @app.errorhandler(APIException)
    def handle_api_exception(error):
        return jsonify({
            "status": "error",
            "message": error.message
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
