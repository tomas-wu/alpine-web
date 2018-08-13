from app.home import blueprint
from flask import render_template, request, json
from flask_login import login_required
from collections import OrderedDict

import numpy as np
import pandas as pd


@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    pjp = OrderedDict([("Select Process", ["Select Project"]),
                      ("110", ["REV1D4", "REV1D5"]),
                      ("120", ["REV2D4", "REV2LP5"]),
                      ("130", ["REV3HRM", "REV3D4"]),
                      ("140", ["REV4D4"]),
                      ("150", ["REV5D5"])
                       ])

	# Default outputs
    process = pjp.keys()[0]
    project = pjp[process][0]
    title = "Project"
    table = "<div class='bg-light text-center' style='height:100px'></p>No Data</p><p>(Select process and project from top-right list)</p></div>"
    submitted = [0, 1]
    metrics = [0, 0, 0, 1]

    if request.method == 'POST':
        process = request.form.get('process')
        project = request.form.get('project')

        if process in pjp.keys()[1:]:
            df = pd.read_csv('test/project.csv')

            submitted = [df["Last Submit"].notna().sum(), df.shape[0]]

            # total = df.shape[0]
            # bar = "<h4>Submitted <font color='blue'>" + "&#x25a0" * int(10 * submitted / total) + "</font>" \
            #       + "<font color='grey'>" + "&#x25a0" * int(10 * (total - submitted) / total) + "</font>" \
            #       + "<small>  %d / %d</small></h4>" % (submitted, total)

            table = df.to_html(index=False, border=0, table_id='metric_table',
                               classes=['table', 'table-striped', 'table-bordered'], na_rep='')

            metrics = [450, 335, 100, 1000]
            title = project

    progress = {"submitted": submitted, "metrics": metrics}
    return render_template('index.html', pjp=pjp, pjp_json=json.dumps(pjp), process=process, project=project, \
                           progress=progress, table=table, title=title, today="9/1/2018")


@blueprint.route('/<project>/<design>')
@login_required
def route_design(project, design):
    df = pd.read_csv('test/%s.csv' % design)
    flag = []
    stat = OrderedDict([("green", 0), ("orange", 0), ("red", 0), ("grey", 0)])
    for i in df.index:
        if df.iloc[i]["Value"] in [str, unicode]:
            flag.append('NA')
            stat["grey"] += 1
        elif df.iloc[i]["Value"] >= df.iloc[i]["Target_Low"] and df.iloc[i]["Value"] <= df.iloc[i]["Target_High"]:
            flag.append('Success')
            stat["green"] += 1
        elif df.iloc[i]["Value"] >= df.iloc[i]["Boundry_Low"] and df.iloc[i]["Value"] <= df.iloc[i]["Boundry_High"]:
            flag.append('Warning')
            stat["orange"] += 1
        else:
            flag.append('Danger')
            stat["red"] += 1

    total = df.shape[0]
    bar = ""
    for k in stat.keys():
        bar += "<font color='%s'>" % k + "&#x25a0"*int(10*stat[k]/total) + "</font>"

    df["Pass"] = flag
    table = df.to_html(index=False, border=0, table_id='metric_table', classes=['table', 'table-striped', 'table-bordered'])
    return render_template('design.html', bar=bar, table=table, subtitle=project, title=design)
    # return json.jsontify(bar=bar, table=table, subtitle=project, title=design)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')