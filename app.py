from flask import Flask, render_template, request, jsonify
import random
import time
import sqlite3

app = Flask(__name__)

teams = ["Jovi Billiot", "Dalton Guidry", "Erik Lane", "Ramey Savoie", "Bryant Lapine", "Grady Fagan", "Jose Gutierrez",
         "Ryan Bruce", "Ryan King", "Trey Foret", "Wesley Martin", "Matthew Leingang"]

topHalfPos = [12, 11, 10, 9, 8, 7]
fourToSix = [6, 5, 4]
topThree = [3, 2, 1]

draftOrderTop = []
draftOrderMid = []
draftOrderLow = []

def generate_draft_order():
    SevenToTwelve()
    time.sleep(1)
    FourToSix()
    time.sleep(1)
    TopThree()

def SevenToTwelve():
    random.shuffle(teams)

    for j in topHalfPos:
        if teams:
            draftOrderTop.append((j, teams.pop(0)))

def FourToSix():
    random.shuffle(teams)

    for i in fourToSix:
        if teams:
            draftOrderMid.append((i, teams.pop(0)))

def TopThree():
    random.shuffle(teams)

    for i in topThree:
        if teams:
            draftOrderLow.append((i, teams.pop(0)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reveal', methods=['POST'])
def reveal():
    conn = sqlite3.connect('draft_order.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS draft_order (
            id INTEGER PRIMARY KEY,
            position INTEGER,
            player_name TEXT
        )
    ''')

    cursor.execute('DELETE FROM draft_order')

    generate_draft_order()
    for order in draftOrderTop + draftOrderMid + draftOrderLow:
        cursor.execute("INSERT INTO draft_order (position, player_name) VALUES (?, ?)", order)

    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/get_draft_order', methods=['GET'])
def get_draft_order():
    conn = sqlite3.connect('draft_order.db')
    cursor = conn.cursor()

    cursor.execute('SELECT position, player_name FROM draft_order ORDER BY position')
    draft_order = cursor.fetchall()

    conn.close()

    return jsonify({'draft_order': draft_order})

if __name__ == '__main__':
    app.run(debug=True)
