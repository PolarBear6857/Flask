import concurrent
import threading

from flask import Flask, render_template, request, jsonify
import json
import bot

# Inicializace aplikace Flask
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Pokusíme se načíst data z JSON souboru, pokud neexistuje, vytvoříme prázdný seznam
try:
    with open('registered_people.json', 'r') as file:
        registered_people = json.load(file)
except Exception:
    registered_people = []


# Pošle email o nové registraci
def send_email():
    global server
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Email configuration
    sender_email = 'testovaciemailjecna@gmail.com'
    receiver_email = 'krupa@spsejecna.cz'
    app_password = 'adlo zwxf nspe vtyl'
    subject = 'Nový uživatel'
    message = 'Právě se registroval nový uživatel'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.quit()


# Hlavní stránka - zobrazuje seznam registrovaných osob
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('prvni_stranka.html', registered_people=registered_people), 200


# Stránka pro registraci nových osob
@app.route('/registrace', methods=['GET', 'POST'])
def druha_stranka():
    return render_template('druha_stranka.html', zprava="Tajná zpráva.."), 200


@app.route('/feedback', methods=['GET', 'POST'])
def treti_stranka():
    return render_template('treti_stranka.html', zprava="Tajná zpráva.."), 200


# Zpracování registrace nové osoby
@app.route('/zpracuj_registraci', methods=['POST'])
def zpracuj_registraci():
    data = request.form

    nick = data.get('nick')
    jmeno = data.get('jmeno')
    prijmeni = data.get('prijmeni')
    pohlavi = data.get('pohlavi')
    je_plavec = data.get('je_plavec')
    kanoe_kamarad = data.get('kanoe_kamarad')

    if je_plavec != '1':
        message = 'Je potřeba umět plavat.'
        status_code = 400
    elif not (nick.isalnum() and 2 <= len(nick) <= 20):
        message = 'Nick musí obsahovat pouze písmena a číslice a mít délku 2 až 20 znaků.'
        status_code = 400
    elif kanoe_kamarad and not (kanoe_kamarad.isalnum() and 2 <= len(kanoe_kamarad) <= 20):
        message = 'Kamarád na lodi musí obsahovat pouze písmena a číslice a mít délku 2 až 20 znaků.'
        status_code = 400
    elif any(person['nick'] == nick for person in registered_people):
        message = 'Toto jméno už je obsazené'
        status_code = 400
    else:
        registered_people.append({
            'nick': nick,
            'jmeno': jmeno,
            'prijmeni': prijmeni,
            'pohlavi': pohlavi,
            'je_plavec': je_plavec,
            'kanoe_kamarad': kanoe_kamarad
        })
        save_data()
        message = 'Registrace byla úspěšně uložena.'
        send_email()
        status_code = 200

    return render_template('druha_stranka.html', message=message), status_code


# API pro ověření dostupnosti jména
@app.route('/api/check-nickname/<nick>', methods=['GET'])
def check_nickname(nick):
    if any(person['nick'] == nick for person in registered_people):
        return jsonify({'exists': True})
    return jsonify({'exists': False})


# Funkce pro uložení dat do JSON souboru
def save_data():
    with open('registered_people.json', 'w') as file:
        json.dump(registered_people, file)


def run_discord_bot():
    bot.run_discord_bot()


def run_flask_app():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    # Create a ThreadPoolExecutor or ProcessPoolExecutor, depending on your preference
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run the functions concurrently
        discord_bot_thread = threading.Thread(target=run_discord_bot)
        discord_bot_thread.start()

        flask_app_thread = threading.Thread(target=run_flask_app)
        flask_app_thread.start()

        # Wait for both threads to finish
        discord_bot_thread.join()
        flask_app_thread.join()
