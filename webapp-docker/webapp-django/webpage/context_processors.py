from .models import Sport, Championship

def sports_context_processor(request):
    return {
        'sports': Sport.objects.all()
    }
    
def championship_context_processor(request):
    return {
        'championship': Championship.objects.all()
    }