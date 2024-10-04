# from django.utils.translation import gettext_lazy as _
# from rest_framework.permissions import AllowAny
#
#
# class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
#     def get_schema(self, request=None, public=False):
#         schema = super().get_schema(request, public)
#         is_secure = request.is_secure()
#         if is_secure:
#             schema.schemes = ["https", "http"]
#         else:
#             schema.schemes = ["http", "https"]
#         return schema
#
#
# schema_view = get_schema_view(
#     Info(
#         title=_("T-MED UZ"),
#         default_version='v1',
#         description=_("checkers description"),
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=Contact(email="contact@snippets.local"),
#         license=License(name="BSD License"),
#     ),
#     public=True,
#     generator_class=BothHttpAndHttpsSchemaGenerator,
#     permission_classes=[AllowAny]
# )
