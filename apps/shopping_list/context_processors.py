def shopping_list_context(request):
    if request.user.is_authenticated:
        return {'shopping_list': request.user.carts.shopping_list}
    return {'shopping_list': request.session.get('shopping_list', [])}
