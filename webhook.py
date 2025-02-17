from quart import Quart, request, jsonify
import os
import json

app = Quart(__name__)
FILE_PATH = 'messages.json'

def init_message_file():
    # Cria o arquivo vazio se ele não existir.
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            f.write("")

def get_next_id():
    # Conta quantas mensagens já foram adicionadas pelo padrão "Id:".
    if not os.path.exists(FILE_PATH):
        return 1
    count = 0
    with open(FILE_PATH, 'r') as f:
        for line in f:
            if line.startswith("Id:"):
                count += 1
    return count + 1

# Inicializa o arquivo antes de definir as rotas
init_message_file()

@app.route('/webhook', methods=['POST'])
async def webhook():
    # Recebe o JSON enviado na requisição
    data = await request.get_json()
    print("SMS recebida:", data)
    
    # Determina o novo id contando mensagens já escritas
    new_id = get_next_id()
    
    # Gera a string com o id e o JSON formatado
    message_lines = []
    message_lines.append(f"Id: {new_id}")
    formatted_message = json.dumps(data, indent=4, ensure_ascii=False)
    message_lines.append(formatted_message)
    # Adiciona o separador ";" ao final
    message_lines.append(";" + "\n")
    mensagem_final = "\n".join(message_lines)
    
    # Acrescenta a nova mensagem no arquivo
    with open(FILE_PATH, 'a') as f:
        f.write(mensagem_final)
    
    return jsonify({'status': 'success', 'message': 'SMS recebida com sucesso.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)