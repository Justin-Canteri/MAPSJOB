#Aca aplico el CRUD para Create, Read, Update y Delete de las ofertas
from ..serializers import jobpostSerializer
from ..models import jobpost, company
#es una clase base de Django REST Framework para crear vistas basadas en clases.
from rest_framework.views import APIView

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from ..permissions import IsEmpresa


#implementar @permission_classes([IsEmpresa]) permisos de emepresas

#solo las empresas pueden usar el post

@api_view(['POST'])
@permission_classes([IsEmpresa])
def post(request):
    serializer = jobpostSerializer(data=request.data)

    if serializer.is_valid():
        #busca en la tabla company si existe una empresa con ese user_id, si no existe tira error
        empresa = company.objects.get(company_id=request.user.id)
        # pasa el objeto empresa para que se autollene en el jobpost
        producto = serializer.save(company_id=empresa)
        return Response(serializer.data, status=201)
        
    # Si falla, registramos la advertencia en consola
    return Response(serializer.errors, status=400)


#Pueden ver u obtener las ofertas disponibles: empresas(con su id), usuarios(todas las disponibles), mapa (las que estan en el area)
#-----------------------------------------------------------------------------------#
@api_view(['GET'])
def get(request):
    resultados = jobpost.objects.all()
    serializer = jobpostSerializer(resultados, many = True)
    return Response(serializer.data)

#Para las empresas que las obtengan por su id
'''
@api_view(['GET'])
@permission_classes([IsEmpresa])
def getID(request):
    try:
        ofertaObtenida = jobpost.objects.get(company_id=request.user.id) #el id de la empresa esta dada por jwt
        serializer = jobpostSerializer(ofertaObtenida)
        return Response(serializer.data)
    except jobpost.DoesNotExist:
        return Response({"error": "No existe"}, status=404)
'''
@api_view(['GET'])
@permission_classes([IsEmpresa])
def getMisOfertas(request):
    try:
        empresa = company.objects.get(company_id=request.user.id)
        ofertas = jobpost.objects.filter(company_id=empresa)
        serializer = jobpostSerializer(ofertas, many=True)
        return Response(serializer.data)
    except company.DoesNotExist:
        return Response({"error": "No existe"}, status=404)
#-----------------------------------------------------------------------------------#

#Las empresas pueden editarlas, solo las con su id por supuesto
@api_view(['PUT'])
@permission_classes([IsEmpresa])
def put(request, id_oferta):
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
@permission_classes([IsEmpresa])
def delete(request, id_oferta):
    try:
        delete_Cat = jobpost.objects.get(id=id_oferta)
        delete_Cat.delete()
            
        return Response({"mensaje": f"Categoría {id_oferta} eliminada"})
    except Exception as e:
            # Esto se enviará automáticamente a errors.log gracias a tu nivel="ERROR"
        return Response({"error": "Error interno al eliminar"}, status=400)