from flask import Flask, request, jsonify
import smtplib
from flask_cors import CORS
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app, origins=["https://seusite.com.br"])

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Dados do formulário
        data = request.get_json()
        nome = data['nome']
        email = data['email']
        empresa = data['empresa']
        mensagem = data['mensagem']
        print('Dados COletados')

        # Configuração do SMTP
        smtp_host = 'smtplw.com.br'
        smtp_user = 'USER'
        smtp_password = 'PASSWORD'
        sender = 'EMAIL_CONFIGURADO'
        print('SMTP configurado')

        # Mensagem para o cliente
        msg_cliente = MIMEText(f"Olá {nome},\n\nObrigado por entrar em contato conosco. Em breve nossa equipe retornara sua mensagem.\n\nAtenciosamente,\nEquipe NEURORA.")
        msg_cliente['Subject'] = 'Recebemos sua mensagem!'
        msg_cliente['From'] = sender
        msg_cliente['To'] = email
        print('Configurando Email Cliente')

        # Mensagem para a empresa
        msg_empresa = MIMEText(f"Novo contato recebido:\n\nNome: {nome}\nE-mail: {email}\nEmpresa: {empresa}\nMensagem: {mensagem}")
        msg_empresa['Subject'] = 'Novo contato recebido'
        msg_empresa['From'] = sender
        msg_empresa['To'] = 'seu_email@suaempresa.com.br' #Email de recepção de dados dos clientes
        print('Configurando Email Empresa')

        # Envia os e-mails
        s = smtplib.SMTP('smtplw.com.br', 587)
        print('iniciando')
        s.set_debuglevel(0)
        s.login(smtp_user, smtp_password)
        s.sendmail(sender, email, msg_cliente.as_string())  # Para o cliente
        s.sendmail(sender, 'seu_email@suaempresa.com.br', msg_empresa.as_string())  # Para a empresa
        s.quit()
        print('Emails Enviados')

        return jsonify({"status": "success"})

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)
