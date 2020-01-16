import regex

with open('books/magyar-ukran-szotar.txt', 'r') as f:
    text = f.readlines()
    new_text = []
    for idx, sentence in enumerate(text):
        match_cyr = regex.match(r'^\p{IsCyrillic}', sentence)
        match_dig = regex.match(r'^\d', sentence)
        match_bra = regex.match(r'^\(', sentence)
        matches = [match_cyr, match_dig, match_bra]
        any_match = next((item for item in matches if item is not None), None)
        if any_match and any_match.start() == 0:
            new_text[-1] = f'{new_text[-1].strip()} {sentence}'
        else:
            new_text.append(sentence)

    # with open('books/magyar-ukran-szotar__.txt', 'w') as s:
    #     s.writelines(new_text)
with open('books/magyar-ukran-szotar_processed.txt', 'r') as so:
    text = so.readlines()
    words = []
    for word in text:
        if not word.startswith(' '):
            values = word.split(' ', 1)
            values = [value.strip() for value in values]
            words.append(values)
    # print(words[1000:1100])



# import psycopg2
#
#
# conn = psycopg2.connect("host=localhost dbname=legyakoribb user=testu password=testp")
#
# cur = conn.cursor()

import pymysql

conn = pymysql.connect(
  host="localhost",
  user="testu",
  passwd="testp",
  database="leggyakoribb"
)
cur = conn.cursor()

# cur.execute("DROP TABLE IF EXISTS hu_ua_dictionary;")
# cur.execute("CREATE TABLE hu_ua_dictionary (id serial PRIMARY KEY, hu_szo varchar, ua_szo varchar);")
cur.execute("SELECT id FROM words_lists WHERE name='HU UA Dictionary'")
res = cur.fetchone()
print(res)

# cur.execute(f"""INSERT INTO words_lists(name, description) VALUES ('HU UA Dictionary', 'Hungarian-Ukrainian dictionary with 5000 words.')""")
# conn.commit()
for word in words:
    if len(word) < 2:
        print(word)
        continue
    cur.execute(f"""INSERT INTO words(hu_szo,ua_szo, words_list_id)
        VALUES
           (
              '{word[0]}',
              '{word[1]}',
              3
           );""")
cur.execute(f"""INSERT INTO users(email, password) VALUES ('atti.dyachok@gmail.com', '12345')""")
cur.execute(f"""INSERT INTO users(email, password) VALUES ('vira.dyachok@gmail.com', '12345')""")
conn.commit()
cur.close()
conn.close()