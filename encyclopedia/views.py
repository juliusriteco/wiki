from random import choice
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import util
from markdown2 import Markdown
markdowner = Markdown()


class NewEntryForm(forms.Form):
    entry = forms.CharField(label="Search", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="New Title", widget=forms.TextInput(attrs={'placeholder': 'Name Page'}))
    body = forms.CharField(label="New Body", widget=forms.Textarea(attrs={'placeholder': 'text space' , 'rows': 3}))

class EditForm(forms.Form):
    title = forms.CharField(label="Edit Title", widget=forms.TextInput(attrs={'placeholder': 'Name Page'}))
    body = forms.CharField(label="Edit Body", widget=forms.Textarea(attrs={'placeholder': 'text space' , 'rows': 3}))



def index(request):
    if request.method == "POST":  # melding van een POST -> activeer
        form = NewEntryForm(request.POST)  # sla melding POST op
        if form.is_valid():  # valide? -> Ga door
            GoToEntry = form.cleaned_data["entry"]  # clean data
            
            if util.get_entry(GoToEntry):  # -> bestaat entry? ga door!
                
                #ga naar pagina encyclopedia:page + parameter title
                return HttpResponseRedirect(reverse("encyclopedia:page", args=[GoToEntry])) 
            
            else:
                # Entry bestaat niet, toon een foutmelding op de searchresults pagina
                return HttpResponseRedirect(reverse("encyclopedia:searchresults", args=[GoToEntry]))
                

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewEntryForm()
    })

def page(request, title):

    
    content = markdowner.convert(util.get_entry(title)) #handmatig content uit entriess halen ahv title
    if content is None:
        return render(request, "encyclopedia/searchresults.html", {
            "message": f"The entry '{title}' was not found."
        })

    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": content,
        "entries": util.list_entries(),
        "form": NewEntryForm()
    })

def searchresults(request, title):
    options = []
    for entry in util.list_entries():
        if title.lower() in entry.lower():
            options.append(entry)

    return render(request, "encyclopedia/searchresults.html", {
        "message": f"The entry '{title}' was not found. Did you mean:",
        "entries": util.list_entries(),
        "form": NewEntryForm(),
        "options": options,
    })

def create(request):
    if request.method == "POST":  # melding van een POST -> activeer
        form = CreateForm(request.POST)  # sla melding POST op
        if form.is_valid():  # valide? -> Ga door
            PageTitle = form.cleaned_data["title"]  # clean data
            PageContent = form.cleaned_data["body"]  # clean data
            if util.get_entry(PageTitle):  # -> bestaat title al? Stop dan!
                return render(request, "encyclopedia/create.html", { 
                    "form_page": form,
                    "error_message": "Already in use",
                })
            else:
                util.save_entry(PageTitle, PageContent)
                return HttpResponseRedirect(reverse("encyclopedia:index")) 
    return render(request, "encyclopedia/create.html", {
        "form_page": CreateForm(),        
        "form": NewEntryForm(),
    })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            PageTitle = form.cleaned_data["title"]
            PageContent = form.cleaned_data["body"]
            util.save_entry(PageTitle, PageContent)
            return HttpResponseRedirect(reverse("encyclopedia:index")) 
        
    content = util.get_entry(title) #handmatig content uit entriess halen ahv title
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
        "edit_form": EditForm(initial={'title':title, "body":content}),
        "form": NewEntryForm(),
    })

def random(request):
    listentries = util.list_entries()
    randomentry = choice(listentries)
    return HttpResponseRedirect(reverse("encyclopedia:page", args=[randomentry])) 