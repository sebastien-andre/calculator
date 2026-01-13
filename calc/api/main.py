from flask import Flask, request, jsonify
from calc.core.session import CalculatorSession
from calc.core.errors import CalcError


def create_app():
    app = Flask(__name__)
    # global session for API
    session = CalculatorSession()
    
    @app.route("/evaluate", methods=["POST"])
    def evaluate():
        data = request.get_json()
        
        if not data or "expression" not in data:
            return jsonify({"error": "Missing 'expression' field"}), 400
        
        expr = data["expression"]
        
        try:
            result = session.evaluate(expr)
            return jsonify({
                "expression": expr,
                "result": result,
                "status": "success"
            }), 200
        except CalcError as e:
            return jsonify({
                "expression": expr,
                "error": str(e),
                "status": "error"
            }), 400

    @app.route("/history", methods=["GET"])
    def get_history():
        # get last 10
        history = session.get_history()
        return jsonify({
            "history": history,
            "count": len(history)
        }), 200

    @app.route("/clear", methods=["POST"])
    def clear_history():
        # clear history
        session.clear_history()
        return jsonify({"status": "success", "message": "History cleared"}), 200

    @app.route("/reset", methods=["POST"])
    def reset():
        # reset calculator state
        session.reset()
        return jsonify({"status": "success", "message": "Calculator reset"}), 200

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app
