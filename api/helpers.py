from rest_framework.validators import ValidationError


def get_or_none(model_class, **kwargs):
    """
    Returns instance of current model class if exists or None
    """
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        ...


def validate_order_status(choices):
    def wrapper(given):
        for choice in choices:
            if given == choice[0]:
                return True
        raise ValidationError('Invalid Order Status')
    return wrapper
