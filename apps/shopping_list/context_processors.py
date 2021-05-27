from shopping_list.models import Purchase


def shopping_list_context(request):
    if request.user.is_authenticated:
        obj, _ = Purchase.objects.get_or_create(user=request.user)
        return {'shopping_list': obj.shopping_list}
    return {'shopping_list': request.session.get('shopping_list', [])}
