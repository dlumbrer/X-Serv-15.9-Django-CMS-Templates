from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

# Create your views here.

@csrf_exempt 
def mostrar(request, recurso):
    #SOLO PUEDES HACER POST SI ESTAS AUTENTICADO
    if request.user.is_authenticated():
        salida = "Eres " + request.user.username + " " + "<a href='/logout'>logout</a>.  Puedes cambiar la page mediante un PUT<br><br>"
        if request.method == "PUT":
            p = Pages(name=recurso, page=request.body)
            p.save()
            return HttpResponse("guardada pagina, haz un get para comprobar")        
    else:
        salida = "No estas logueado <a href='/admin/login/'>Login</a>. No puedes cambiar la page<br><br>"
    

    try:
        fila = Pages.objects.get(name=recurso)
        salida += request.method + " " + str(fila.id) + " " + fila.name + " " + fila.page
        return HttpResponse(salida)
    except Pages.DoesNotExist:
        salida += "Page not found: " + recurso
        return HttpResponseNotFound(salida)

@csrf_exempt         
def mostrartemplate(request, recurso):
    #SOLO PUEDES HACER POST SI ESTAS AUTENTICADO
    if request.user.is_authenticated():
        salida = "Eres " + request.user.username + " " + "<a href='/logout'>logout</a>.  Puedes cambiar la page mediante un PUT<br><br>"
        if request.method == "PUT":
            p = Pages(name=recurso, page=request.body)
            p.save()
            return HttpResponse("guardada pagina, haz un get para comprobar")        
    else:
        salida = "No estas logueado <a href='/admin/login/'>Login</a>. No puedes cambiar la page<br><br>"
    

    try:
        fila = Pages.objects.get(name=recurso)
        salida += request.method + " " + str(fila.id) + " " + fila.name + " " + fila.page
        
        #PLANTILLA###########
        # 1. Indicar la plantilla a utilizar
        plantilla = get_template('blue.html')
        # 2. Definir el contexto
        # MUY IMPORTANTE EN EL INDEX DEBE DE HABER LAS ETIQUETAS {{ title }} y {{ contenido }}, MIRAR EN marioz/index.html
        c = Context({'title': recurso, 'contenido': salida, 'user': request.user.username,})
        # 3. Renderizar
        renderizado = plantilla.render(c)
        return HttpResponse(renderizado)
    except Pages.DoesNotExist:
        salida += "Page not found: " + recurso
        return HttpResponseNotFound(salida)


def todo(request):
    if request.user.is_authenticated():
        salida = "Eres " + request.user.username + " " + "<a href='/logout'>logout</a><br><br>"
    else:
        salida = "No estas logueado <a href='/admin/login/'>Login</a><br><br>"
            
    lista = Pages.objects.all()
    salida += "Esto es lo que tenemos:<ul>"
    for fila in lista:
        salida += "<li>" + fila.name + "->" + str(fila.page) + " "
    salida += "</ul>"
    return HttpResponse(salida)
