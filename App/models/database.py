from App import db


def insert_into_cards(preprocessed_cards):
    for card_no in preprocessed_cards:
        query_preamble = f"INSERT INTO CARD_{card_no} VALUES(NULL"
        query_postamble = ");"
        for entry in preprocessed_cards[card_no]:
            query = query_preamble
            for field in entry:
                query = query + f", \"{entry[field]}\""
            query = query + query_postamble
            db.session.execute(query)
    db.session.commit()
