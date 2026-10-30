from flask import Blueprint, abort, current_app, request

from .services import dostepne_regiony, policz_wskazniki
from flask import abort
from .services import raporty_roku # upewnij się, że masz tu też importy z poprzednich zajęć (np. dostepne_regiony)
from flask import request, redirect, url_for, abort
from .services import zapisz_raport
panel_bp = Blueprint("panel", __name__)


@panel_bp.get("/")
def index():
    return "Panel wskaźników"


@panel_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    if region is not None and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")
    w = policz_wskazniki(sciezka, region)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    return f"<h1>Wskaźniki: {w['region'] or 'wszystkie'}</h1><p>Marża: {w['marza']:.2%}</p>"

@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if kod not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {kod}")
    
    # Tutaj wstaw wywołanie funkcji z poprzednich zajęć liczącej zamówienia
    liczba = 3 # (Zastąp to właściwą funkcją)
    return f"<h1>Region {kod}</h1><p>Zamówień: {liczba}</p>"


ROK_DOMYSLNY = 2026

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"

 # upewnij się, że masz ten import

@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "<p>Instrukcja: Wyślij żądanie POST, aby zapisać raport.</p>"
    
    # Odczyt danych z POST
    rok = request.form.get("rok", type=int)
    region = request.form.get("region")
    
    # 1. Walidacja: brak liczby lub zły region
    # (Zakładam, że dostepne_regiony to funkcja, którą poprawiliśmy w Zadaniu 1)
    if rok is None or region not in ["PL","DE","CZ"]:
        abort(400, description="Niepoprawne dane formularza")
        
    # 2. Walidacja: rok poza zakresem
    if not (2020 <= rok <= 2030):
        abort(422, description="Rok poza zakresem 2020-2030")
        
    # 3. Zapis i przekierowanie 303 (Post/Redirect/Get)
    zapisz_raport(rok, region)
    return redirect(url_for("panel.raport", rok=rok), 303)

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)
