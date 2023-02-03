from datetime import datetime


def year(request):
    dt = datetime.now().year
    return {"year": dt}


def welcome(request):
    """Добавляет в контекст переменную greeting с приветствием."""
    return {
        "greeting": "Ennyn Pronin: pedo mellon a minno.",
    }
