from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

def convt_md_html(title):
      cdata = util.get_entry(title)
      markdowner = Markdown()
      if cdata == None:
        return None
      else:
        return markdowner.convert(cdata)
      
def index(request):
      
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
  html_content = convt_md_html(title)
  if html_content == None:
    return render(request, "encyclopedia/error.html", {
      "message": "Your Request does not exist"
    })
  else:
    return render(request, "encyclopedia/entry.html",{
      "title": title,
      "cdata": html_content
      })

def search(request):
  if request.method == "POST":
    entry_search = request.POST['q']
    html_content = convt_md_html(entry_search)
    if html_content is not None:
      return render(request, "encyclopedia/entry.html",{
        "title": entry_search,
        "cdata": html_content
      })
    
    else:
      allEntries = util.list_entries()
      recomend = []
      for entry in allEntries:
        if entry_search.lower() in entry.lower():
          recomend.append(entry)
          
      return render(request, "encyclopedia/search.html",{
        "recomend": recomend,
      })
      
def new_pg(request):
  if request.method == "GET":
    return render(request, "encyclopedia/new.html")
  else:
    title = request.POST['title']
    cdata = request.POST['cdata']
    titleExist = util.get_entry(title)
    if titleExist is not None:
      return render(request, "encyclopedia/error.html", {
        "message": "Entered page already exists"
      })
    else:
      util.save_entry(title, cdata)
      html_content = convt_md_html(title)
      return render(request, "encyclopedia/entry.html",{
        "title": title,
        "cdata": html_content
      })
     
def edit(request):
  if request.method == 'POST':
    title = request.POST['entry_title']
    cdata = util.get_entry(title)
    return render(request, "encyclopedia/edit.html",{
       "title": title,
        "cdata": cdata
    })
    
def save_edit(request):
   if request.method == 'POST':
     
    title = request.POST['title']
    cdata = request.POST['cdata']
    util.save_entry(title, cdata)
    html_content = convt_md_html(title)
    return render(request, "encyclopedia/entry.html",{
       "title": title,
        "cdata": html_content
    })
    
def rand(request):
  allEntries = util.list_entries()
  rand_entry = random.choice(allEntries)
  html_content = convt_md_html(rand_entry)
  return render(request, "encyclopedia/entry.html",{
    "title": rand_entry,
    "cdata": html_content
    })
    
