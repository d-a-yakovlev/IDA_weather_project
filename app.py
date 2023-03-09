import base64
from flask import Flask, render_template, request

from data.Storage import Storage
from utillity_modules.Estimator import  Estimator 
from utillity_modules.GeoPainter import GeoPainter


PATH_TO_GRAPHS = "./static/graphs/"
#storage = Storage()
app = Flask(__name__)


@app.route('/')
def index():
    #cities = storage.get_cities()
    
    #заглушка
    cities = ['Москва', 'Санкт-Петербург', 'Ульяновск', 'Иркутск', 'Спасёновск']
    
    context = {
        'cities' : cities,
    }
    return render_template("index.html", **context)


@app.route('/forecast')
def forecast():
    city = request.args['city']
    days = request.args['days']
    detail = request.args['detail']

    ## Примерное видение того как будут работать ваши модули

    # estimator = Estimator(city=city, storage=Storage)
    # predictions = estimator.forecast(days=days, save_graph=True)
    # GeoPainter(predictions, city=city, days=days).paint()

    # stats = estimator.get_stats()
    # detailed_stats = None
    # if detail == 'true':
    #     detailed_stats = estimator.get_detailed_stats()

    with open(PATH_TO_GRAPHS + "estimator_graph.png", "rb") as img_file:
        estimator_graph_base64 = base64.b64encode(img_file.read()).decode("ascii")

    with open(PATH_TO_GRAPHS + "geo_painter_graph.png", "rb") as img_file:
        geo_painter_graph_base64 = base64.b64encode(img_file.read()).decode("ascii")

    # заглушки
    stats = ['среднее 322', 'дисперсия 228', 'квантиль квантилей']
    detailed_stats = ['квантильный квантиль квантилей', 'p-value того что завтра не будет дедлайнов']
    
    context = {
        'stats' : stats,
        'detailed_stats' : detailed_stats,
        'estimator_graph_base64' : estimator_graph_base64,
        'geo_painter_graph_base64' : geo_painter_graph_base64
    }
    return render_template("draw_forecast.html", **context)


if __name__ == "__main__":
    app.run(
        host="localhost",
        debug=True
    )