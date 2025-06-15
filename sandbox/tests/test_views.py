
from django.urls import path
from rest_framework import status
from rest_framework.test import APIClient

import pytest
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular_extras.views import SpectacularScalarView

urlpatterns_v2 = [
    path("api/v2/schema/scalar/", SpectacularScalarView.as_view(), name="scalar"),
]
urlpatterns_v2.append(
    path("api/v2/schema/", SpectacularAPIView.as_view(urlconf=urlpatterns_v2), name="schema"),
)

urlpatterns = urlpatterns_v2


@pytest.mark.parametrize("ui", ["scalar"])
@pytest.mark.urls(__name__)
def test_spectacular_ui_view(ui):
    from drf_spectacular_extras.settings import spectacular_extras_settings
    response = APIClient().get(f"/api/v2/schema/{ui}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.content.startswith(b"<!DOCTYPE html>")
    if ui == "scalar":
        assert b"<title>Scalar</title>" in response.content
        assert spectacular_extras_settings.SCALAR_DIST.encode() in response.content

    assert b'"/api/v2/schema/"' in response.content

