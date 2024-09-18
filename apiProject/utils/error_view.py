from django.http import JsonResponse




def handler404(request, exception): #اذا سوا ريقويست وطلع ايرور يعطيه ايش هوا الايرور
   message = ('path not found')
   response = JsonResponse(data={'error':message})
   response.status_code = 404
   return response


def handler500(request, exception): #اذا سوا ريقويست وطلع ايرور يعطيه ايش هوا الايرور
   message = ('Internal server error')
   response = JsonResponse(data={'error':message})
   response.status_code = 500
   return response