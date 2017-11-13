from django.shortcuts import render


def home_page(request):
    """
    Handles http request to the home page
    """
    return render(request, 'home.html',
                  {'new_item_text': request.POST.get('item_text', '')})
