#Aca aplico el CRUD para Create, Read, Update y Delete de las ofertas
from serializers import jobpostSerializer
from models import jobpost
#es una clase base de Django REST Framework para crear vistas basadas en clases.
from rest_framework.views import APIView

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes


#solo las empresas pueden usar el post

@api_view(['POST'])
def post(self, request):
    serializer = jobpostSerializer(data=request.data)

    if serializer.is_valid():
        producto = serializer.save()
        return Response(serializer.data, status=201)
        
    # Si falla, registramos la advertencia en consola
    return Response(serializer.errors, status=400)


#Pueden ver u obtener las ofertas disponibles: empresas(con su id), usuarios(todas las disponibles), mapa (las que estan en el area)
#-----------------------------------------------------------------------------------#
@api_view(['GET'])
def get(self, request):
    resultados = jobpost.objects.all()
    serializer = jobpostSerializer(resultados, many = True)
    return Response(serializer.data)

#Para las empresas que las obtengan por su id
@api_view(['GET'])
def getID(self, request, id_empresa):
    try:
        ofertaObtenida = jobpost.objects.get(id=id_empresa) #el id de la empresa esta dada por jwt
        serializer = jobpostSerializer(ofertaObtenida)
        return Response(serializer.data)
    except jobpost.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

#-----------------------------------------------------------------------------------#

#Las empresas pueden editarlas, solo las con su id por supuesto
@api_view(['PUT'])
def put(self, request, id_oferta):
    try:
        categoria_Obtenido = jobpost.objects.get(id=id_oferta)
        serializer = jobpostSerializer(categoria_Obtenido, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=400)
    except jobpost.DoesNotExist:
        return Response({"error": "No existe"}, status=404)

#las empresas pueden eliminarlas, con su id por supuesto
@api_view(['DELETE'])
def delete(self, request, id_oferta):
    try:
        delete_Cat = jobpost.objects.get(id=id_oferta)
        nombre_cat = delete_Cat.category_name
        delete_Cat.delete()
            
        return Response({"mensaje": f"Categoría {id_oferta} eliminada"})
    except Exception as e:
            # Esto se enviará automáticamente a errors.log gracias a tu nivel="ERROR"
        jobpost.error(f"Error crítico al eliminar categoría {id_oferta}: {str(e)}")
        return Response({"error": "Error interno al eliminar"}, status=400)