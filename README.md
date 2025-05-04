# FuricoBot - Assistente Telegram para fãs da FURIA CS

## Autor: Lucas Giazzi

**FuricoBot** é um bot desenvolvido para o Telegram com o objetivo de fornecer informações interativas sobre o time de **Counter-Strike da FURIA**. Ele utiliza a API da OpenAI para responder com uma linguagem descontraída, porém informativa, mantendo o foco no universo competitivo do CS.

---

## Funcionalidades

- Respostas automáticas baseadas em palavras-chave sobre o time da FURIA CS.
- Integração com o modelo GPT da OpenAI para respostas contextuais mais completas.
- Comando `/start` para iniciar a interação com o bot.
- Arquivo `faq.json` para manutenção facilitada das respostas fixas.

---

## Tecnologias Utilizadas

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- OpenAI API (GPT-3.5 Turbo)
- dotenv
- JSON

---

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados:

- Python 3.10 ou superior
- Pip (gerenciador de pacotes do Python)
- Conta na OpenAI para obter a chave da API
- Conta no Telegram para criar um bot e obter o token

---

## Instalação e Configuração

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/furicobot.git
   cd furicobot
   2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` na raiz do projeto e adicione as variáveis de ambiente necessárias:
   ```env
   TELEGRAM_TOKEN=seu_token_do_telegram
   OPENAI_API_KEY=sua_chave_da_openai
   ```

4. Certifique-se de que o arquivo `.env` está listado no `.gitignore` para evitar o vazamento de credenciais.

---

## Como Usar

1. Execute o bot:
   ```bash
   python main.py
   ```

2. No Telegram, inicie uma conversa com o bot e use o comando `/start` para começar.

3. Envie mensagens ou áudios relacionados ao time da FURIA para obter respostas.

4. **Nota**: A funcionalidade de identificação de áudio está em desenvolvimento e pode não funcionar corretamente em todos os casos.

---

## Estrutura do Projeto

```plaintext
├── main.py               # Arquivo principal do bot
├── requirements.txt      # Dependências do projeto
├── .env                  # Configurações sensíveis (não incluído no repositório)
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Documentação do projeto
├── data/
│   └── faq.json          # Respostas fixas baseadas em palavras-chave
```

---

## Licença

Este projeto é de uso exclusivo para fins educacionais e demonstração de habilidades técnicas.
