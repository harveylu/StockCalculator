# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
from myproject.settings import PROJECT_ROOT
import stockcalculate

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def graph(request):
    json_data = open(os.path.join(PROJECT_ROOT, '../static/project_result.json'))
    print type(json_data)
    data1 = json.load(json_data)
    print type(data1)
    # data2 = json.dumps(json_data)
    # print type(data2)
    json_data.close()
    return render(request, 'graph.html', {'result': data1})


def result(request):
    # testing = {
    #     "stock": "aapl",
    #     "strategy": "Ethical Investing "
    # }
    return render(request, 'report-error.html',{'result': 'Submit a new set of data to get your report!'})


def submit(request):
    if request.method == 'POST':
        print request.POST.get('price')
        print request.POST.get('checkbox')
        print request.POST
        checkbox1 = assignbool(request.POST.get('checkbox1'))
        checkbox2 = assignbool(request.POST.get('checkbox2'))
        checkbox3 = assignbool(request.POST.get('checkbox3'))
        checkbox4 = assignbool(request.POST.get('checkbox4'))
        checkbox5 = assignbool(request.POST.get('checkbox5'))
        print type(float(request.POST.get('price')))
        print type(checkbox1)
        print type(checkbox2)
        print type(checkbox3)
        print type(checkbox4)
        print type(checkbox5)
        testing = {
            "stock": request.POST.get('price'),
            "checkbox1": checkbox1,
            "checkbox2": checkbox2,
            "checkbox3": checkbox3,
            "checkbox4": checkbox4,
            "checkbox5": checkbox5
        }
        print request.POST.get('checkbox1')
        print request.POST.get('checkbox2')
        print request.POST.get('checkbox3')
        print request.POST.get('checkbox4')
        print request.POST.get('checkbox5')
        json_result = stockcalculate.investment_with_strategy(float(request.POST.get('price')), checkbox1, checkbox2, checkbox3, checkbox4, checkbox5)
        # json_data = open(os.path.join(PROJECT_ROOT, '../static/project_result.json'))
        # data1 = json.load(json_data)
        # json_data.close()
        if "error" in json_result:
            print "Error detected"
            # print data1
            return render(request, 'report-error.html', {'result': json_result['error']})
        else:
            # print type(json_data)
            print type(json_result)
            # print(json.dumps(json_result, indent=2, sort_keys=False))
            # print "Type of result is" + type(json_result)
            # data2 = json.dumps(json_data)
            # print type(data2)
            return render(request, 'result.html', {'result': json_result})


def assignbool(val):
    if val == "on":
        return True
    else:
        return False
