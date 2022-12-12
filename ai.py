import openai
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'test'

@app.route("/", methods=["GET", "POST"])
def key():
    if "api_key" in session:
        openai.api_key = session["api_key"]
        return render_template("home.html")
    if request.method == "POST":
        thekey = request.form.get("keybox")
        session["api_key"] = thekey
        openai.api_key = session["api_key"]
        return render_template("home.html")
    return render_template("key.html")
    
@app.route("/home", methods=["GET", "POST"])
def home():
        return render_template("home.html")

@app.route("/image", methods=["GET", "POST"])
def image():
    if request.method == "POST":
        prompt = request.form.get("promptbox")
        size = request.form.get("size")
        image = createimage(prompt, size)
        return render_template("image.html", image=image)
    return render_template("image.html")

@app.route("/text", methods=["GET", "POST"])
def text():
    if request.method == "POST":
        prompt = request.form.get("promptbox")
        temp = request.form.get("temperaturebox")
        text = textcompletion(prompt, float(temp))
        return render_template("text.html", text=text)
    return render_template("text.html")

def createimage(prompt, size):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size= size,
    )
    return(response.data[0].url)

def textcompletion (prompt, temperature):
    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        temperature=temperature,
        max_tokens=400,
    )
    return(response.choices[0].text)

if __name__ == '__main__':
    app.run(host="localhost", port=8284, debug=True)
