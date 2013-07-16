from flask import Flask, request, render_template
import candy_flask

app = Flask(__name__)
farm = candy_flask.Farm()
player = candy_flask.Player(farm)


@app.route('/', methods= ['GET'])
def index():
    return render_template("index.html")

@app.route('/game', methods=['POST'])
def game():
    resp = request.form['command']
    global player 
    result = player.play(resp)
    avai_actions = player.show_menu()
    return render_template('game.html', result=result, avai_actions=avai_actions)

if __name__== '__main__':
    app.run(debug=True)



