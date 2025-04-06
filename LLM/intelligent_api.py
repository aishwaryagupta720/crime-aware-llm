# app.py
from flask import Flask, request, jsonify, Response
from llm_handler import get_response
import logging

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def analyze_prompt():
    prompt = request.json.get('prompt')
    logging.info("hello im here")
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    content, status_code, content_type = get_response(prompt)
    if status_code == 200:
        return Response(content, status=200, mimetype=content_type)
    else:
        return jsonify({'error': content}), status_code

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
