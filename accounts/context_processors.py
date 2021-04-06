def favourites_count(request):
    """
    Custom context processor for user favourites list count.
    """
    if request.user.is_authenticated:
        return {'favourites_count':request.user.favourites.count()} 
    else:
        return {'favourites_count':0}     