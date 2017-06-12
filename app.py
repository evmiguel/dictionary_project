from flask import Flask
import os.path

app = Flask(__name__)

@app.route('/add_entry')
def add_entry(word,definition):
    file = False

    if(not os.path.isfile("gre_words.csv")):
        file = open('gre_words.csv', 'w+')
        file.write("entry,definition\n")
    else:
        file = open('gre_words.csv', 'a')

    file.write(word+","+definition+"\n")
    file.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
