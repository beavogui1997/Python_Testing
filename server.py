import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = next((club for club in clubs if club['email'] == request.form['email']), None)
    if club:
       today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       return render_template('welcome.html',club=club,competitions=competitions, today_date=today_date)
    else:
        flash("Erreur: Adresse e-mail non trouvée dans la liste des clubs.")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=foundCompetition)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.form['places'] is "":
        flash("Renseigner le nombre de places svp")
        return render_template('welcome.html', club=club, competitions=competitions, today_date=today_date)
    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash("Erreur: impossible de faire une reservation de plus de 12 places.")
        return render_template('welcome.html', club=club, competitions=competitions, today_date=today_date)
    if int(club['points']) < placesRequired:
        flash("Erreur: vous n'avez assez de points pour un tel nombre de places.")
        return render_template('welcome.html', club=club, competitions=competitions, today_date=today_date)
    if (int(competition['numberOfPlaces']) - placesRequired) < 0:
        flash("Erreur: concours déjà complet, plus de reservation.")
        return render_template('welcome.html', club=club, competitions=competitions, today_date=today_date)
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = str(int(club['points']) - placesRequired)
        flash(f"Réservation terminée aves succès, {placesRequired} places ont été achétées.")
        return render_template('welcome.html', club=club, competitions=competitions, today_date=today_date)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)