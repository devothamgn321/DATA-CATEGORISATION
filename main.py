import csv

from flask import Flask

#
#   split_data_to_cards(data_file_path)
#
#   parameters:
#       data_file_path : string - is the file path (relative/absolute) to the data csv file
#   return:
#       a dictionary that maps card number (string) to a list of data rows corresponding to that card
#
def split_data_to_cards(data_file_path):
    cards = {}

    with open(data_file_path,'r') as file:
        for line in file:
            if not cards.get(line[17]):
                cards[line[17]] = []
            cards[line[17]].append(line)

    return cards

#
#   get_line_lookup(lookup_file_path)
#
#   parameters:
#       lookup_file_path : string - is the file path (relative/absolute) to the lookup csv file
#   return:
#       a dictionary of the following format
#           card_no(string) -> dict(variable_name(string) -> [start_col, end_col, dict(code -> value)])
#
def get_line_lookup(lookup_file_path):
    with open(lookup_file_path, 'r') as file:
        cards_datatype = {}
        var_name = 0
        card_no = 1
        start_idx = 2
        end_idx = 3
        lookup = 4
        val = 5

        reader = csv.reader(file)
        next(reader)    # ignore the header

        for row in reader:
            if not cards_datatype.get(row[card_no]):
                # if cards_datatype doesn't have an entry for a card number, initialize it to an empty dictionary
                cards_datatype[row[card_no]] = {}
            if not cards_datatype[row[card_no]].get(row[var_name]):
                # if we encounter a new variable name for that card's datatype, make a new entry of the format
                # [start_col, end_col + 1, empty dictionary], note that both start_col and end_col are in zero
                # based indexing.
                cards_datatype[row[card_no]][row[var_name]] = [int(row[start_idx])-1, int(row[end_idx]), {}]
            # if we encounter an existing variable name, then we add the new code to the dictionary in the
            # third entry of the list and map it to the corresponding value.
            cards_datatype[row[card_no]][row[var_name]][2][row[lookup]] = row[val]

    return cards_datatype

#
#   process_cards(cards, cards_datatype)
#
#   parameters:
#       card : a dictionary of the format returned by split_data_to_cards
#       cards_datatype: a dictionary of the format returned by get_line_lookup
#   return:
#       a dictionary that maps the corresponding attributes to its value
#
def process_cards(cards, cards_datatype):
    processed = {}
    for key in cards.keys():
        processed[key] = []    # for every card empty array is created '1':[], '2':[], '3':[], '4':[]}

    for key in cards.keys():
        for entry in cards[key]:
            ans = {}
            for var_name in cards_datatype[key]:
                attribs = cards_datatype[key][var_name] #key = card num
                ans[var_name] = attribs[2].get(entry[attribs[0]:attribs[1]],entry[attribs[0]:attribs[1]])
            processed[key].append(ans)

    return processed

#
#   write_proceesed_cards_to_file(processed)
#
#   parameters:
#       processed : a dictionary of type returned by process_cards()
#   return:
#       None. Instead generates CSV files for each card in the dataset.
#
def write_proceesed_cards_to_file(processed):
    for card_no in processed.keys():
        with open(f'card{card_no}.csv', 'w', newline='') as d:
            writer = csv.writer(d)
            header = []
            for key in processed[card_no][0].keys():
                header.append(key)
            writer.writerow(header)

            for entry in processed[card_no]:
                row = []
                for key in entry.keys():
                    row.append(entry[key])
                writer.writerow(row)


if __name__ == '__main__':
   cards = split_data_to_cards("C:\\Users\\gnd-nts\\Downloads\\Radio_Audiences_Survey_Responses_Q1.csv")
   lookup_dict = get_line_lookup("C:\\Users\\gnd-nts\\Downloads\\Radio_Survey_Data_Lookup_Q1.csv")
   processed = process_cards(cards, lookup_dict)
   print(processed['1'][0].keys())
   #write_proceesed_cards_to_file(processed)
