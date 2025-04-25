# 💻 Web Scraping Dashboard - MyTek & Tunisianet

Ce projet est une application web complète qui scrape en temps réel les ordinateurs portables disponibles sur les sites **MyTek** et **Tunisianet**, les filtre selon différents critères, et les affiche dans une interface conviviale avec images, prix, lien d'achat et disponibilité.

---

## 🚀 Fonctionnalités principales

- 🔍 **Filtrage dynamique** : par **marque**, **processeur**, **prix minimum**, **prix maximum**
- 🛒 **Scraping en temps réel** avec `Selenium` + `undetected-chromedriver`
- 📈 **Visualisation claire** des produits avec disponibilité, image, prix, source, et lien
- 🧠 Gestion des erreurs : Affichage du message *"Aucun produit trouvé"* si aucun résultat ne correspond
- ⚡ Interface utilisateur dynamique avec `JavaScript`, `HTML` et `CSS`
- 🌐 Serveur `Flask` pour gérer les requêtes filtrées en AJAX

---

## 🧰 Technologies utilisées

- 🐍 Python 
- 🔎 Selenium + undetected-chromedriver
- 📊 Pandas
- 🌐 Flask
- 🎨 HTML/CSS/JavaScript

---

## 📦 Installation

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python app.py
