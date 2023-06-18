from flask import Flask, request, render_template
import main

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def terminal(text_area=""):
    try:
        if request.form["eqc"]:
            eqc = request.form["eqc"]
            equacao = main.Solver(eqc)
            return render_template("terminal.html", resultado=equacao.retorna_resultado(), conta=equacao.retorna_conta())
    except:
        return render_template("terminal.html", resultado="", conta="")

if __name__ == "__main__":
    app.run(debug=True)
