from flask import Flask, render_template, request
import pandas as pd
import cufflinks as cf
import plotly as py

app = Flask(__name__)

df = pd.read_csv('total2.csv', encoding='utf-8')
regions_available_loaded = list(df.ComponentName.dropna().unique())


cf.set_config_file(offline=True, theme="ggplot")


@app.route('/', methods=['GET'])
def people_income():
    data_str = df.to_html()
    regions_available = regions_available_loaded
    return render_template('results2.html',
                           the_res=data_str,
                           the_select_region=regions_available)

@app.route('/', methods=['POST'])
def people_select() -> 'html':
    the_region = request.form["the_region_selected"]
    print(the_region)

    dfs = df.query("ComponentName=='{}'".format(the_region))

    data_str = dfs.to_html()

    fig = dfs.iplot(kind="bar", x="GeoName", y="data", asFigure=True)
    py.offline.plot(fig, filename="result.html", auto_open=False)
    with open("result.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    regions_available = regions_available_loaded

    return render_template('results2.html',
                           the_plot_all= plot_all,
                           the_res=data_str,
                           the_select_region=regions_available,
                           )


if __name__ == '__main__':
    app.run(port=8071)



