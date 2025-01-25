from flask import Flask, render_template, request, redirect, url_for
import threading
import imap_server
import queue

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/final')
def final():
    return render_template('final.html')

def start_email_retrieval(email):
    try:
        imap_server.retrieve_email(email)
    except Exception as e:
        print(f"Error retrieving email for {email}: {e}")

@app.route('/confirm_forwarding', methods=['POST'])
def confirm_forwarding():
    try:
        email = request.form['user_email']
        thread = threading.Thread(target=start_email_retrieval, args=(email,))
        thread.start()
        return redirect(url_for('final'))
    except Exception as e:
        print(f"Error confirming forwarding: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
