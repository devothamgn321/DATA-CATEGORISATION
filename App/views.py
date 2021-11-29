from App import app, db
from flask import render_template, request, flash, redirect, send_file
from werkzeug.utils import secure_filename
from App.controllers.CardParser import split_data_to_cards, get_line_lookup, process_cards
from App.models.database import insert_into_cards
import os
import pandas as pd

card_responses_filename = None
card_responses = {}
card_lookup_filename = None
card_lookup_table = get_line_lookup(os.path.join(app.config['RES_FOLDER'], "Radio_Survey_Data_Lookup_Q1.csv"))

@app.route('/')
def home():
    card1 = db.session.execute("select * from card_1;")
    card2 = db.session.execute("select * from card_2;")
    card3 = db.session.execute("select * from card_3;")
    card4 = db.session.execute("select * from card_4;")
    card6 = db.session.execute("select * from card_6;")

    card_headers = []
    for idx in card_lookup_table:
        header = ['ID']
        for key in card_lookup_table[idx]:
            header.append(key)
        card_headers.append(header)

    return render_template(
        "home.html",
        cards=[card1, card2, card3, card4, card6],
        card_headers=card_headers,
        card_names=["Card_1", "Card_2", "Card_3", "Card_4", "Card_6"]
    )

@app.route('/upload', methods=['POST'])
def upload_and_process():
    global card_lookup_filename
    global card_lookup_table
    global card_responses
    global card_responses_filename
    if request.method == 'POST':
        if 'response_file' not in request.files:
            flash('Please add response')
            return redirect('/')

        if request.files['response_file'].filename == '':
            flash('Please add response')
            return redirect('/')

        response_file = request.files['response_file']

        if response_file and secure_filename(response_file.filename):
            card_responses_filename = secure_filename(response_file.filename)
            response_file.save(os.path.join(app.config['UPLOAD_FOLDER'], card_responses_filename))

            card_responses = split_data_to_cards(os.path.join(app.config['UPLOAD_FOLDER'], card_responses_filename))
            card_lookup_table = get_line_lookup(os.path.join(app.config['RES_FOLDER'], "Radio_Survey_Data_Lookup_Q1.csv"))

            preprocess = process_cards(card_responses, card_lookup_table)
            insert_into_cards(preprocess)
            return redirect('/')
        else:
            flash('Failed to upload file')
            return redirect('/')

    else:
        response.status(405)

@app.route('/download', methods=['POST'])
def download():
    table_name_lookup = {
        "Card_1": "card_1",
        "Card_2": "card_2",
        "Card_3": "card_3",
        "Card_4": "card_4",
        "Card_6": "card_6"
    }

    card = list(db.session.execute(f"select * from {table_name_lookup[request.form['card_id']]};"))
    header = ['ID']
    for key in card_lookup_table[request.form['card_id'][-1]]:
        header.append(key)

    card_df = pd.DataFrame(card, columns=header)
    filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], "download.xlsx")
    writer = pd.ExcelWriter(filepath)
    card_df.to_excel(writer, sheet_name="Sheet 1")
    writer.save()

    return send_file("download\\download.xlsx")