from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .context_global import pic_global

@login_required 
def index(request):
    return render(request, 'menu.html', pic_global(request))
