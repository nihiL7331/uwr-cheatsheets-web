from django.conf import settings


def site_name(req):
    return {"site_name": settings.SITE_NAME}
