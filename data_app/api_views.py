from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
@csrf_exempt
@require_POST
def get_token(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    print(email, password)
    user = authenticate(request, email=email, password=password)
    print(user)
    if user is not None:
        # Generate token and return it
        token = user.auth_token.key
        return JsonResponse({'token': token})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


# update