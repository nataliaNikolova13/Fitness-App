from django.shortcuts import render

# Create your views here.
def homePage(request):
    return render(request, 'common/core.html')

def custom_404(request, exception):
    return render(request, 'common/notFound.html', status=404)