from django.http import JsonResponse

def charge(request):
    if request.method == 'POST':
        # Add your Stripe logic here
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
