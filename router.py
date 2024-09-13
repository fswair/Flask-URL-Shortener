from flask import Flask, redirect, render_template, request
from main import Shortener

app  = Flask(__name__, template_folder="temps")


@app.route("/")
def home():
    return render_template("front.html")

@app.route("/<urlid>")
def route_url(urlid):
    shortener = Shortener(short_url=urlid).__get__(param=urlid)
    if shortener.is_url:
        return redirect(shortener.link)
    return "Its not a valid URL..Maybe, link expired you want to see.."

@app.route("/redirect", methods = ["post"])
def add_link():
    if request.method == "POST":
        url = request.form.get("url")
        alias = request.form.get("alias")
        
        try:is_alias_on = True if request.form.get("is_alias_on") == "on" else False
        except:is_alias_on = False

        shortener = Shortener(link=url, alias=alias if is_alias_on else "", is_active=1, has_alias=is_alias_on)
        if shortener.is_alias_exists(_alias = alias):
            return "Alias exists."
        short_url = shortener.create_short_url()
        shortener.short_url = short_url
        shortener.alias = short_url if not shortener.alias else alias
        shortener.__add__()

        link = Shortener(short_url=short_url).__get__()
        return redirect(f"{request.root_url}show/{link.short_url}")
    return redirect(request.root_url)

@app.route("/show/<short_url>")
def show_url(short_url):
    shortener = Shortener(short_url=short_url, alias=short_url).__get__()
    if shortener.is_active:
        locate = shortener.short_url or shortener.alias
        return f"Successfully created link for <a href='{shortener.link}'>this</a> web address.\nThis link <a href='{request.root_url}{locate}'>{request.root_url}{locate}</a>, will redirect web page, you specified."
    return "Link expired." 
