from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

import random

'''
class NewEntry(forms.Form):
    title = forms.CharField()
    body = forms.Textarea()
    '''

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "found":True,
            "title":title.capitalize(),
            "entry":entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "found":False,
            "title":title
        })

def search(request):
    query = request.GET['q']
    entry = util.get_entry(query)
    if entry is not None:
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[query]))
    else:
        entries = util.list_entries()
        results = []
        for entry in entries:
            entry = entry.lower()
            if (entry.find(query.lower()) >= 0):
                results.append(entry)
        if results:
            return render(request, "encyclopedia/result.html", {
                "found":True,    
                "query":query,
                "results": results
                })
        else:
            return render(request, "encyclopedia/result.html", {
                "found":False,
                "query":query
                })

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create.html", {
                "message":f"An entry with title '{title}' already exists. Try another one.",
                "title":title,
                "content":content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    return render(request, "encyclopedia/create.html")

def randompage(request):
    entries = util.list_entries()
    n=0
    for entry in entries:
        n+=1
    i = random.randint(1,n)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entries[i-1]]))

def edit(request, title):
    entry = util.get_entry(title)
    return HttpResponseRedirect(reverse("encyclopedia:create", kwargs={
        "title": title,
        "content": entry
    }))