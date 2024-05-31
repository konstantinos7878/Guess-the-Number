from flask import Flask, render_template, request
from random import randint


app = Flask(__name__)

# Ανοίγουμε την αρχική σελίδα
@app.route('/')
def index():
    return render_template('index.html')

# Συνάρτηση επιλογής του τυχαίου αριθμού και προβολής της σελίδας με το παιχνίδι.
@app.route('/main/game/', methods=['POST', 'GET'])
def game():
    tries = 7
    number = randint(0, 100)
    return render_template('game.html', number=number, tries=tries, value="", bnumber1="", bnumber2="", bnumber3="",
                                bnumber4="", bnumber5="", snumber1="", snumber2="", snumber3="", snumber4="", snumber5="")
            

# Βασική συνάρτηση παιχνιδιού
@app.route('/main/game/update_value/', methods=['POST'])
def main_game():
    value = request.form.get('value', '')               # Διαβάζουμε την τιμή που εχει εισάγει ο χρήστης νωρίτερα, καθώς και
    button_value = request.form.get('btn_num', '')      # την τιμή του κουμπιού. Σε περίπτωση που δεν βρεθούν οι τιμές επιστρέφει "".
    # ελέγχουμε αν έχει εισάγει 3 χαρακτήρες (δεν έχει νόημα να εισάγει περισσότερους)
    if len(value)>=3:
        new_value=value

    else:
        new_value = value + button_value

    # Είσοδος μεταβλητών    
    number = request.form.get('number')
    tries = request.form.get('tries')
    tries = int(tries)
    bnumber1 = request.form.get('bnumber1')
    bnumber2 = request.form.get('bnumber2')
    bnumber3 = request.form.get('bnumber3')
    bnumber4 = request.form.get('bnumber4')
    bnumber5 = request.form.get('bnumber5')

    snumber1 = request.form.get('snumber1')
    snumber2 = request.form.get('snumber2')
    snumber3 = request.form.get('snumber3')
    snumber4 = request.form.get('snumber4')
    snumber5 = request.form.get('snumber5')

    bigger_numbers = [bnumber1, bnumber2, bnumber3, bnumber4, bnumber5]
    smaller_numbers = [snumber1, snumber2, snumber3, snumber4, snumber5]

    
    if button_value =="clear":
        new_value = ""
    if (button_value == "enter"):
        # ελέγχουμε αν η είσοδος είναι κενή
        if value=="":
            new_value=""
        # Περίπτωση νίκης
        elif(value == number):
            score = 1000/7*tries
            with open('stats.txt', 'a') as file:
                file.write(f"Won! number: {number} , score: {score:.0f}\n")
            return render_template('result.html', message=f"Congratulations! You found the number! Your score: {score:.0f}")
        # Περίπτωση λανθασμένης προσπάθειας
        else:
            tries=tries-1
            if(tries == 0):
                with open('stats.txt', 'a') as file:
                    file.write(f"Lost! number: {number} , score: 0\n")
                return render_template('result.html', message=f"You lost! The number was: {number}. Your score: 0")
            else:
                # Έλεγχος για το αν ο αριθμός εισόδου είναι μεγαλύτερος ή μικρότερος από τον αριθμό του προγράμματος
                if int(value)>int(number):
                    # Βρίσκουμε τη πρώτη κενή θέση στη λίστα, ώστε να προβάλουμε με τη σειρά τους λανθασμένους αριθμούς
                    for i in range(5):
                        if smaller_numbers[i]=="":
                            smaller_numbers[i]=value
                            break
                else:
                    for i in range(5):
                        if bigger_numbers[i]=="":
                            bigger_numbers[i]=value
                            break
            # Αρχικοποίηση της τιμής της εισόδου
            new_value=""
    return render_template('game.html', number=number, tries=tries, value=new_value, bnumber1=bigger_numbers[0], bnumber2=bigger_numbers[1]
                           , bnumber3=bigger_numbers[2], bnumber4=bigger_numbers[3], bnumber5=bigger_numbers[4],
                             snumber1=smaller_numbers[0], snumber2=smaller_numbers[1], snumber3=smaller_numbers[2],
                               snumber4=smaller_numbers[3], snumber5=smaller_numbers[4])


# Συνάρρτηση υπεύθυνη για την προβολή των στατιστικών
@app.route('/main/stats', methods=['POST'])
def stats():
    with open('stats.txt', 'r') as file:
        statistics = file.readlines()
    return render_template('stats.html', statistics = statistics)


if __name__ == '__main__':
    app.run(debug=True)


