from flask import Flask, render_template, redirect, url_for
import sqlite3
import honeypot
import requests

app = Flask(__name__)

honeypot.init_db()

def get_logs():
    conn = sqlite3.connect('attacks.db')
    conn.row_factory = sqlite3.Row
    logs = conn.execute(
        "SELECT * FROM incidents ORDER BY id DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return logs

def system_status():
    return honeypot.running

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('home.html', status=system_status())

# تشغيل النظام
@app.route('/start')
def start():
    honeypot.start_honeypot()
    return redirect(url_for('home'))

# إيقاف النظام
@app.route('/stop')
def stop():
    honeypot.stop_honeypot()
    return redirect(url_for('home'))

# الداشبورد
@app.route('/dashboard')
def dashboard():
    return render_template('index.html', attacks=get_logs())

# توليد هجوم (اختياري للاختبار)
@app.route('/attack/<int:port>')
def attack(port):
    try:
        requests.get(f"http://localhost:{port}")
    except:
        pass
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
