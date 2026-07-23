from django.shortcuts import render
from os import listdir
from os.path import isfile, join
from pathlib import Path
import os
from .model_run import model_run_script

def get_files(dir):
    if not dir or not os.path.isdir(dir):
        
        return []
    onlyfiles = [os.path.join(dir, f) for f in os.listdir(dir) if 
                 os.path.isfile(os.path.join(dir, f))]
    model_run_script(onlyfiles)
    return onlyfiles
# Create your views here.


    
# Page codes


def home(request):
       folder_path = request.GET.get("path", "")
       files=get_files(folder_path)
    
       return render(request, "home.html", {
        "folder_path": folder_path
    })

def load(request):
       return render(request, "load.html")