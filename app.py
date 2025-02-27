from flask import Flask, render_template, request
import aiohttp
import asyncio
import os
import logging

app = Flask(__name__)

# Configuração do log
app.logger.setLevel(logging.ERROR)

# Função assíncrona para gerar o código
async def gerar_codigo(linguagem, descricao):
    url = "http://localhost:11434/api/generate"
    prompt = f"Escreva um código em {linguagem} que {descricao}"
    data = {"model": "codellama", "prompt": prompt, "stream": False}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            result = await response.json()
            return result["response"]

# Função para rodar de forma assíncrona com Flask
def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

@app.route('/', methods=['GET', 'POST'])
def index():
    codigo = ""
    if request.method == 'POST':
        linguagem = request.form['linguagem']
        descricao = request.form['descricao']
        # Limpar o console antes de rodar o processo
        os.system('cls')  # 'cls' se estiver no Windows
        codigo = run_async(gerar_codigo, linguagem, descricao)
    return render_template('index.html', codigo=codigo)

if __name__ == '__main__':
    app.run(debug=False)  # Desabilitar debug para produção
