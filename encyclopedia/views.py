from django.shortcuts import render

from . import util


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