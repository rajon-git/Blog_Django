from django.shortcuts import render,redirect
from . import forms

# Create your views here.
def add_category(request):
    if request.method == 'POST':
        category_forms = forms.CategoryForm(request.POST)
        if category_forms.is_valid():
            category_forms.save()
            return redirect('add_category')
    else:
        category_forms = forms.CategoryForm()
    return render(request, 'add_category.html',{'form': category_forms})