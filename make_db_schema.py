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
   lookup_dict = get_line_lookup("C:\\Users\\gnd-nts\\Downloads\\Radio_Survey_Data_Lookup_Q1.csv")

   print(lookup_dict.keys())
   print(lookup_dict['1'])
   print(lookup_dict['1'].keys())

   for card_no in lookup_dict.keys():
       query_str = f"""
        CREATE TABLE CARD_{card_no} (
            id MEDIUMINT NOT NULL AUTO_INCREMENT,
       """

       for field_name in lookup_dict[card_no]:
           filtered_field_name = field_name.replace(' ', '_').replace('/', '_').replace('-', '_').replace('.', '')
           query_str = query_str + f"{filtered_field_name} VARCHAR(200),"

       query_str = query_str + "PRIMARY KEY(id));"

       print(query_str)

   #
   # CREATE TABLE CARD_n (
   #    id AUTO_INCREMENT NOT NULL,
   #    field_name VARCHAR(size)
   #    .
   #    .
   #    .
   #    PRIMARY KEY(id)
   #    );

   # CREATE
   # TABLE
   # CARD_2(
   #     id
   # MEDIUMINT
   # NOT
   # NULL
   # AUTO_INCREMENT,
   # DIARY_YEAR
   # VARCHAR(200), DIARY_WEEK
   # VARCHAR(200), SAMPLE_POINT
   # VARCHAR(200), ADDRESS_SERIAL_NUMBER
   # VARCHAR(200), PERSON_NUMBER
   # VARCHAR(200), CARD_NUMBER
   # VARCHAR(200), SEX
   # VARCHAR(200), WORKING_STATUS
   # VARCHAR(200), EXACT_AGE_LAST_BIRTHDAY
   # VARCHAR(200), MAIN_SHOPPER
   # VARCHAR(200), UNDERSTANDS_WELSH
   # VARCHAR(200), NUMBER_OF_DAYS_WATCH_TV_IN_AVERAGE_WEEK
   # VARCHAR(200), HOURS_WATCH_TV_ON_AVG_WEEKDAY
   # VARCHAR(200), HOURS_WATCH_TV_ON_AVG_WEEKEND_DAY
   # VARCHAR(200), WEIGHT_OF_VIEWING_ALL_TELEVISION
   # VARCHAR(200), SPEAK_WELSH_FLUENTLY
   # VARCHAR(200), MARITAL_STATUS
   # VARCHAR(200), ARE_YOU_THE_PARENT_OR_GUARDIAN_OF_ANYONE_IN_THIS_HOUSEHOLD
   # VARCHAR(200), ARE_YOU_THE_CHILD_OR_DEPENDENT_OF_ANYONE_IN_THIS_HOUSEHOLD
   # VARCHAR(200), RESPONDENT_WEIGHTING_FACTOR
   # VARCHAR(200), DO_YOU_OWN_A_MOBILE_PHONE
   # VARCHAR(200), DO_YOU_OWN_A_SMARTPHONE
   # VARCHAR(200), DO_YOU_USE_ANY_OF_THE_FOLLOWING_WEBSITE_APPS
   # VARCHAR(200), FREQUENCY_USE_LISTEN_AGAIN
   # VARCHAR(200), NATIONAL_NEWSPAPERS
   # VARCHAR(200), FREQUENCY_USE_FACEBOOK
   # VARCHAR(200), FREQUENCY_USE_FLICKR
   # VARCHAR(200), FREQUENCY_USE_INSTAGRAM
   # VARCHAR(200), FREQUENCY_USE_LINKEDIN
   # VARCHAR(200), FREQUENCY_USE_MESSENGER
   # VARCHAR(200), FREQUENCY_USE_PINTEREST
   # VARCHAR(200), FREQUENCY_USE_SNAPCHAT
   # VARCHAR(200), FREQUENCY_USE_TUMBLR
   # VARCHAR(200), FREQUENCY_USE_TWITTER
   # VARCHAR(200), FREQUENCY_USE_YOUTUBE
   # VARCHAR(200), FREQUENCY_USE_WHATSAPP
   # VARCHAR(200), ETHNIC_ORIGIN
   # VARCHAR(200), DO_YOU_OR_ANYONE_IN_YOUR_HOUSEHOLD_OWN_A_TV VARCHAR(200), AUTHORISED_BUSINESS_SPEND
   # VARCHAR(200), PAST_YEAR_BUSINESS_SPEND_OVER_5000
   # VARCHAR(200), DAB_SET_OWNED_IN_HOME
   # VARCHAR(200), FREQUENCY_LISTEN_TO_PODCASTS
   # VARCHAR(200), RESPONDENT_IS_SELF_EMPLOYED
   # VARCHAR(200), LISTEN_TO_RADIO_VIA_HEADPHONES
   # VARCHAR(200), FREQUENCY_OF_CINEMA_GOING
   # VARCHAR(
   #     200), DO_YOU_HAVE_ANY_LONG_TERM_DISABILITY_HEALTH_PROBLEM_OR_ILLNESS VARCHAR(
   #     200), TYPE_OF_DISABILITY
   # VARCHAR(200), IPSOS_USE_ONLY
   # VARCHAR(200), FREQUENCY_OF_LISTENING_TO_THE_RADIO
   # VARCHAR(200), FREQUENCY_OF_LISTENING_TO_THE_RADIO_AT_HOME
   # VARCHAR(200), FREQUENCY_OF_LISTENING_TO_THE_RADIO_AT_WORK
   # VARCHAR(200), FREQUENCY_OF_LISTENING_TO_THE_RADIO_MOBILE
   # VARCHAR(200), FREQUENCY_OF_LISTENING_TO_THE_RADIO_TABLET
   # VARCHAR(200), OWN_ACTSPEAKER VARCHAR(
   #     200), FREQUENCY_OF_LISTENING_TO_THE_RADIO_ACTSPEAKER VARCHAR(
   #     200), FREQUENCY_OF_GENERAL_ACCESS_TO_THE_INTERNET VARCHAR(
   #     200), FREQUENCY_OF_LISTENING_TO_THE_RADIO_VIA_A_TV_SET VARCHAR(
   #     200), FREQUENCY_OF_LISTENING_TO_ON_DEMAND_MUSIC_SERVICES
   # VARCHAR(200), DO_YOU_USE_A_SMART_SPEAKER VARCHAR(
   #     200), WHICH_OF_THE_FOLLOWING_DO_YOU_USE_A_SMART_SPEAKER_FOR VARCHAR(200), POSITION_HELD_AT_WORK
   # VARCHAR(200), RESPONSIBILITY_OF_PURCHASE_DECISION_AT_WORK
   # VARCHAR(200), NUMBER_OF_EMPLOYEES_IN_THE_COMPANY_YOU_WORK_FOR
   # VARCHAR(200), PRIMARY
   # KEY(id));
