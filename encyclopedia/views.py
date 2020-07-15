from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            'found':True,
            'title':title,
            'entry':content
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'found':False,
            'title':title
        })

def search(request, query=None):
    if (query is not None) or (request.method == 'POST'):
        if request.method == 'POST':
            qry = request.POST.get('q')
        else:
            qry = query
        entry = util.get_entry(qry)
        if entry is not None:
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[qry]))
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                entry = entry.lower()
                if (entry.find(qry.lower()) >= 0):
                    results.append(entry)
            if results:
                return render(request, "encyclopedia/result.html", {
                    "found":True,    
                    "query":qry,
                    "results": results
                    })
            else:
                return render(request, "encyclopedia/result.html", {
                    "found":False,
                    "query":qry
                    })
    else:
        return render(request, 'encyclopedia/search.html')

def randompage(request):
    entries = util.list_entries()
    n=0
    for entry in entries:
        n+=1
    i = random.randint(1,n)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entries[i-1]]))

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create_entry.html", {
                "message":f"An entry with title '{title}' already exists. Try another one.",
                "title":title,
                "content":content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    else:
        return render(request, "encyclopedia/create_entry.html")