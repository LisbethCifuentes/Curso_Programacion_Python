from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Pet
import json


def serialize_pet(pet):
    """Serializa un objeto Pet a diccionario"""
    return {
        "id": str(pet.id),
        "name": pet.name,
        "species": pet.species,
        "age": pet.age,
        "owner": pet.owner,
        "vaccinated": pet.vaccinated,
    }


# ==================== VISTA RENDERIZADA (SIN AUTH) ====================
def pets_page(request):
    """Vista HTML renderizada - NO requiere autenticación"""
    pets = Pet.objects.all()
    return render(request, 'pets/pets_list.html', {'pets': pets})


# ==================== API CRUD (CON JWT) ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pets_api_list(request):
    """
    GET: Lista todas las mascotas (con filtros opcionales)
    POST: Crea una nueva mascota
    """
    if request.method == 'GET':
        pets = Pet.objects.all()
        
        # Filtros opcionales
        species = request.GET.get('species')
        vaccinated = request.GET.get('vaccinated')
        
        if species:
            pets = pets.filter(species=species)
        
        if vaccinated is not None:
            pets = pets.filter(vaccinated=(vaccinated.lower() == 'true'))
        
        serialized_pets = [serialize_pet(pet) for pet in pets]
        return Response(serialized_pets, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        data = request.data
        
        # Validación básica
        required_fields = ['name', 'species', 'age', 'owner']
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Field "{field}" is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            pet = Pet.objects.create(
                name=data['name'],
                species=data['species'],
                age=int(data['age']),
                owner=data['owner'],
                vaccinated=data.get('vaccinated', False)
            )
            
            return Response(
                {
                    'message': 'Pet created successfully',
                    'pet': serialize_pet(pet)
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def pets_api_detail(request, pet_id):
    """
    GET: Obtiene una mascota específica
    PUT: Actualiza una mascota
    DELETE: Elimina una mascota
    """
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        return Response(serialize_pet(pet), status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        data = request.data
        
        # Actualizar campos
        if 'name' in data:
            pet.name = data['name']
        if 'species' in data:
            pet.species = data['species']
        if 'age' in data:
            pet.age = int(data['age'])
        if 'owner' in data:
            pet.owner = data['owner']
        if 'vaccinated' in data:
            pet.vaccinated = data['vaccinated']
        
        pet.save()
        
        return Response(
            {
                'message': 'Pet updated successfully',
                'pet': serialize_pet(pet)
            },
            status=status.HTTP_200_OK
        )
    
    elif request.method == 'DELETE':
        pet.delete()
        return Response(
            {'message': 'Pet deleted successfully'},
            status=status.HTTP_200_OK
        )