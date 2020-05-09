import base64
import io
import json
from cmath import pi, cos
from django.core.serializers.json import DjangoJSONEncoder
from matplotlib import pylab
from pandas.io.json import json_normalize
from pylab import *
import PIL, PIL.Image
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pan
from bs4 import BeautifulSoup, Tag
from IPython.display import HTML, display
import matplotlib as mat


# Create your views here.
from matplotlib.pyplot import plot, xlabel, ylabel, title, grid
from numpy.ma import arange



def loaddata(request):

    df = pan.read_csv('http://localhost/1000SalesRecords.csv').head(50)

    df = df.to_html()
   # print(type(df))
    df = df.replace('dataframe', 'table')
    df = df.replace('<table border="1" class="table"','<table border="1" class="table" id="tt" style=""')
    #print(df)


    f = open('App1/templates/App1/home.html', 'w')
    f2 = open('App1/templates/App1/HomeDesign.html', 'r')
    design = f2.read()
   # htmlcode='<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><head><link crossorigin="anonymous" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" rel="stylesheet"/><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script></head><title>Shoping Cart Analyser</title><body><div class="container"><table border="1" class="table"><nav class="navbar navbar-inverse"><div class="container-fluid"><div class="navbar-header"><a class="navbar-brand" href="#">Shoping Cart Analyzer</a></div><ul class="nav navbar-nav"><li class="active"><a href="#">Home</a></li><li><a href="http://127.0.0.1:8000/Plot/">Plot</a></ul></div></nav>'+ df +'</div></body>'+Maxup + '</html>'

    htmlcode = design + df + '</div></body></html>'

    soup = BeautifulSoup(htmlcode, features="html.parser")
    tag = soup.find("thead")
    tag['class'] = "thead-dark"


    tag2 = soup.find("table")
    #if (tag2['class']=="table"):
     #   tag2['id']="table"
      #  soup.table.e


    soup.thead.replaceWith(tag)

    tag = soup.find("table")
    tag['class'] = "table"

    soup.table.replaceWith(tag)
    htmlcode = str(soup)

    f.write(htmlcode)
    f.close()


    content = {'Title': 'Super Market Data Analyzer', 'DataFrame': df}


    return render(request, 'App1/home.html', content)


def getimage(request):
    # Construct the graph
    df = pan.read_csv('http://localhost/1000SalesRecords.csv').head(50)

    x = (df['Unit Price']).head(10).tolist()
    s = (df['Unit Cost']).head(10).tolist()
    c = (df['Units Sold']).head(10).tolist()
    x.sort()
    s.sort()
    c.sort()
    

    plt.plot(x,s)
    plt.plot(x, s, 'r--', s, s, 'bs')
    plt.plot(x, c)


    xlabel('Unit Price')
    ylabel('Unit Cost')
    title('Shopping Cart Graph!')
    grid(True)
    plt.savefig('App1/1stgraph.png')

    plt.show()

    html="<html><h1 href='file:///C:/Users/Shubham/PycharmProjects/Test/Test/App1/1stgraph.png'>The image is saved.<h1></html>"
    return render(request, 'App1/home.html')


def analyze(request):
    df = pan.read_csv('http://localhost/1000SalesRecords.csv').head(50)

    itemtypelist = df['Item Type'].value_counts().to_frame().to_html()

    soup = BeautifulSoup(itemtypelist, features="html.parser")
    tag = soup.find("thead")

    tag['class'] = "thead-dark"

    soup.thead.replaceWith(tag)

    tag = soup.find("table")
    tag['class'] = "table"

    soup.table.replaceWith(tag)
    itemtypelist = str(soup)
    itemtypelist = itemtypelist.replace('Item Type','Number of Products')


    fr = open('App1/templates/App1/DesignReport.html', 'r')
    report = fr.read()

    f = open('App1/templates/App1/analysis.html', 'w')
    f2 = open('App1/templates/App1/HomeDesign.html', 'r')
    design = f2.read()
    f.write(report +itemtypelist+ '</html>')
    f.close()

    mostregion = list(df['Region'].mode())
    xx=''
    mostregion= xx.join(mostregion)   # Most Common Region

    mostcountry = list(df['Country'].mode())
    xx=''
    mostcountry= xx.join(mostcountry)   # Most Common Country

    oloff = df['Sales Channel'].value_counts().tolist()
    totall = sum(oloff)
    ol = oloff[0]
    olpercent = long((ol / totall) * 100)
   # offpercent = 100-olpercent

    totalprofit = sum(df['Total Profit'])
    totalprofit = long(totalprofit)


    content={'maxunitprice': max(df['Unit Price']),'maxprofit':max(df['Total Profit']),'mostregion':mostregion, 'Name':'The Shopping Cart Analyzer',
             'mostcountry': mostcountry, 'totalprofit':totalprofit, 'olpercent':olpercent}

    return render(request, 'App1/analysis.html',content)