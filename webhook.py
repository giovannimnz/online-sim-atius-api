from quart import Quart, request, jsonify
import os
import json

app = Quart(__name__)
FILE_PATH = 'messages.json'

def init_message_file():
    # Cria o arquivo JSON com uma lista vazia, se ele não existir.
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            json.dump([], f)

# Inicializa o arquivo antes de definir as rotas
init_message_file()

@app.route('/webhook', methods=['POST'])
async def webhook():
    # Obtém o JSON enviado na requisição
    data = await request.get_json()
    print("SMS recebida:", data)

    # Carrega as mensagens existentes
    with open(FILE_PATH, 'r') as f:
        messages = json.load(f)

    # Define o novo id baseado no número de mensagens existentes
    new_id = len(messages) + 1

    # Obtém o conteúdo da mensagem, com valor padrão se não existir
    message_text = data.get('message', 'Mensagem sem conteúdo')

    # Adiciona a nova mensagem à lista
    messages.append({"id": new_id, "message": message_text})

    # Salva a lista atualizada no arquivo JSON com identação
    with open(FILE_PATH, 'w') as f:
        json.dump(messages, f, indent=4)

    # Retorna resposta de sucesso
    return jsonify({'status': 'success', 'message': 'SMS recebida com sucesso.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)