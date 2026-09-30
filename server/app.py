import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
SPIDER_API_KEY = os.environ.get('SPIDER_API_KEY')

def obter_modelo_groq():
    headers = {'Authorization': f'Bearer {GROQ_API_KEY}'}
        preferencias = [
                "llama-3.3-70b-versatile",
                        "llama-3.1-8b-instant",
                                "openai/gpt-oss-120b",
                                        "qwen/qwen3.8-27b"
                                            ]
                                                try:
                                                        res = requests.get('https://api.groq.com/openai/v1/models', headers=headers, timeout=10)
                                                                if res.status_code == 200:
                                                                            disponiveis = [m['id'] for m in res.json().get('data', [])]
                                                                                        for pref in preferencias:
                                                                                                        if pref in disponiveis:
                                                                                                                            return pref
                                                                                                                                        if disponiveis:
                                                                                                                                                        return disponiveis[0]
                                                                                                                                                            except Exception as e:
                                                                                                                                                                    print(f"[*] Erro ao buscar modelos Groq: {e}")
                                                                                                                                                                        return "llama-3.1-8b-instant"

                                                                                                                                                                        @app.route('/gerar', methods=['POST'])
                                                                                                                                                                        def gerar():
                                                                                                                                                                            dados = request.get_json() or {}
                                                                                                                                                                                prompt = dados.get('prompt', '')
                                                                                                                                                                                    
                                                                                                                                                                                        if not prompt:
                                                                                                                                                                                                return jsonify({'error': 'Prompt vazio'}), 400
                                                                                                                                                                                                        
                                                                                                                                                                                                            modelo = obter_modelo_groq()
                                                                                                                                                                                                                headers = {
                                                                                                                                                                                                                        'Authorization': f'Bearer {GROQ_API_KEY}',
                                                                                                                                                                                                                                'Content-Type': 'application/json'
                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                        payload = {
                                                                                                                                                                                                                                                'model': modelo,
                                                                                                                                                                                                                                                        'messages': [{'role': 'user', 'content': prompt}]
                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                            res = requests.post('https://api.groq.com/openai/v1/chat/completions', json=payload, headers=headers, timeout=30)
                                                                                                                                                                                                                                                                                    if res.status_code == 200:
                                                                                                                                                                                                                                                                                                resposta = res.json()['choices'][0]['message']['content']
                                                                                                                                                                                                                                                                                                            return jsonify({'resposta': resposta})
                                                                                                                                                                                                                                                                                                                    return jsonify({'error': f'Erro API Groq: {res.status_code}'}), res.status_code
                                                                                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                                                                                return jsonify({'error': str(e)}), 500

                                                                                                                                                                                                                                                                                                                                if __name__ == '__main__':
                                                                                                                                                                                                                                                                                                                                    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))