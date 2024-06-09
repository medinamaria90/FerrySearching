from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SearcherForm
from .services import SupplierManager

# This view renders the index.HTML doc.
def index(request):
    if request.method == "POST":
        form_searcher = SearcherForm(request.POST)
        ship_summary = SupplierManager(form_searcher).get_all_suppliers()
        ship_departures = ship_summary.get('departures', [])
        ship_returns = ship_summary.get('returns', [])
        if not ship_departures:
            messages.info(
                request, "Sorry, there isn't any Ferry service for the departure date.")
        elif not ship_returns and ship_returns != None:
            messages.info(
                request, "Sorry, there isn't any Ferry service for the return date.")
        return render(request, "index.html", {'form': form_searcher, 'ship_departures': ship_departures, 'ship_returns': ship_returns})
    else:
        form_searcher = SearcherForm()
    return render(request, "index.html", {'form': form_searcher})
