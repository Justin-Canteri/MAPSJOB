import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

#importa la base de datos
from base.models import users, company, jobpost

#por si la transicion a las bases de datos falla
from django.db import transaction


#permisos
from rest_framework.decorators import api_view, permission_classes

#para que al registrarse por ejemplo una empresa se le asigne al grupo automaticamnete
from django.contrib.auth.models import Group


#registro de usuario
#@api_view(['POST']) ya se encarga de rechazar cualquier request que no sea POST, devolviendo un 405 Method Not Allowed automáticamente
@api_view(['POST'])
@csrf_exempt
def registrar_usuario(request):
        try:
            datos = request.data
            
            # Solo pedimos lo básico para la cuenta
            username = datos.get('username')
            email = datos.get('email', '')
            password = datos.get('password')

            if not username or not password or not email:
                return JsonResponse({"error": "Usuario, contraseña y email son obligatorios"}, status=400)

            # Así si uno falla, el otro se revierte también y no quedan datos a medias.
            # el transaction.atomic es para eso, verificar que todo se envie 
            with transaction.atomic():
                # Crear el usuario (contraseña encriptada automáticamente)

                nuevo_usuario = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_active= True
            )
                #Mando a la otra base de datos realcionada "users"
                users.objects.create(
                user_id=nuevo_usuario,
                apellido=datos.get('apellido'),
                phone=datos.get('phone'),
                is_active = True,
                fecha_nacimiento = datos.get('fecha_nacimiento'),
                direccion = datos.get('direccion'),
                curriculum = datos.get('curriculum')
            )
    

            #cambiar
            return JsonResponse({
                "mensaje": "Usuario creado. Ahora un administrador debe asignarle un rol.",
                "id": nuevo_usuario.id,
                "username": nuevo_usuario.username
            }, status=201)

        except IntegrityError:
            return JsonResponse({"error": "El nombre de usuario ya existe"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



#registro de empresa

#@api_view(['POST']) ya se encarga de rechazar cualquier request que no sea POST, 
# devolviendo un 405 Method Not Allowed automáticamente
# y tambien Parsea el body automáticamente y lo deja disponible en request.data ( osea no necesita el
#data = json.load(request.data), eso cargaria de nuevo el json devolviendo error)
@api_view(['POST'])
@csrf_exempt
def registrar_empresa(request):
    
        try:
            datos = request.data
            
            # Solo pedimos lo básico para la cuenta
            username = datos.get('username')
            password = datos.get('password')
            email = datos.get('email', '')

            if not username or not password:
                return JsonResponse({"error": "completa los campos"}, status=400)


            with transaction.atomic():
                # Crear el usuario (contraseña encriptada automáticamente)
                nueva_empresa = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                )

                #Mando a la otra base de datos realcionada "users"
                company.objects.create(
                    company_id=nueva_empresa,
                    description = datos.get('description'),
                    website = datos.get('website'),
                    phone = datos.get('phone'),
                    direccion = datos.get('direccion'),
                    verified = False
                )
                grupo = Group.objects.get(name='IsEmpresa')
                nueva_empresa.groups.add(grupo)

            #cambiar
            return JsonResponse({
                "mensaje": "Usuario creado. Ahora un administrador debe asignarle un rol.",
                "id": nueva_empresa.id,
                "username": nueva_empresa.username
            }, status=201)

        #Exacto, esa es una lección importante — siempre poné el except Exception 
        # antes del except IntegrityError mientras estás desarrollando, así ves el error real.
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        except IntegrityError:
            return JsonResponse({"error": "El nombre de usuario ya existe"}, status=400)
