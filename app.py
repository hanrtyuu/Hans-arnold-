
from flask import Flask, request, render_template_string, redirect
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)

DOSSIER = Path("images_recues")
DOSSIER.mkdir(exist_ok=True)

PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Image à partager</title>
<style>
body {
    background: #101827;
    color: white;
    font-family: Arial;
    text-align: center;
    padding: 30px 15px;
}
img {
    width: 100%;
    max-width: 350px;
    border-radius: 15px;
}
button {
    background: #1687ff;
    color: white;
    padding: 15px;
    border: 0;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
</head>
<body>
<h2>Image à partager</h2>
<img src="/image" alt="Image">
<p>Souhaites-tu partager une image avec le propriétaire de ce lien ?</p>
<form action="/recevoir" method="POST"
enctype="multipart/form-data">
<input type="file" name="photo" accept="image/*" required>
<br>
<button type="submit">Confirmer l'envoi</button>
</form>
</body>
</html>
"""

@app.route("/")
def accueil():
    return render_template_string(PAGE)

@app.route("/image")
def image():
    from flask import send_from_directory
    return send_from_directory(".", "image.jpg")

@app.route("/recevoir", methods=["POST"])
def recevoir():
    photo = request.files.get("photo")

    if not photo or not photo.filename:
        return "Aucune image sélectionnée", 400

    if not photo.mimetype.startswith("image/"):
        return "Format non autorisé", 400

    nom = secure_filename(photo.filename)
    destination = DOSSIER / nom

    i = 1
    while destination.exists():
        destination = DOSSIER / f"{i}_{nom}"
        i += 1

    photo.save(destination)
    return "Image reçue avec succès !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

