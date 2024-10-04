from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.utils.translation import gettext_lazy as _

# Schema for AboutUsGenericAPIView
about_us_schema = extend_schema_view(
    get=extend_schema(
        tags=['about-us'],
        summary=_('About Us details'),
        description=_('Retrieve the details for About Us section'),
    )
)

# Schema for StructureListAPIView
structure_schema = extend_schema_view(
    get=extend_schema(
        tags=['structure'],
        summary=_('List&Detail structure'),
        description=_('Get the list of structures'),
    )
)

# Schema for LawListAPIView
law_schema = extend_schema_view(
    get=extend_schema(
        tags=['laws'],
        summary=_('List&Detail laws'),
        description=_('Get the list of laws'),
    )
)

# Schema for OrganizationsViewSet
organizations_schema = extend_schema_view(
    list=extend_schema(
        tags=['organization'],
        summary=_('List organizations'),
        description=_('Retrieve a list of all organizations')
    ),
    retrieve=extend_schema(
        tags=['organization'],
        summary=_('Detail organizations'),
        description=_('Retrieve detail of any organization')
    ),

    products=extend_schema(
        tags=['organization'],
        summary=_('List organization services'),
        description=_('Retrieve a list of products for a specific organization')
    ),
    product_detail=extend_schema(
        tags=['organization'],
        summary=_('Detail organization services'),
        description=_('Retrieve details of a specific product by ID for an organization'),
    ),
    specialists=extend_schema(
        tags=['organization'],
        summary=_('List organization specialists'),
        description=_('Retrieve a list of specialists for a specific organization')
    ),
    specialist_detail=extend_schema(
        tags=['organization'],
        summary=_('Detail organization specialist'),
        description=_('Retrieve specialist details')
    )
)

# Schema for ManagementReadOnlyModelViewSet
management_schema = extend_schema_view(
    list=extend_schema(
        tags=['management'],
        summary=_('List&Detail management entries'),
        description=_('Retrieve a list of management entries'),
    ),
    retrieve=extend_schema(
        tags=['management'],
        summary=_('Retrieve a management entry'),
        description=_('Retrieve detailed management entry by ID'),
    )
)

# Schema for ContentReadOnlyModelViewSet
content_schema = extend_schema_view(
    list=extend_schema(
        tags=['contents'],
        summary=_('List&Detail contents'),
        description=_('Retrieve a list of contents'),
    ),
    retrieve=extend_schema(
        tags=['contents'],
        summary=_('Retrieve content'),
        description=_('Retrieve detailed content entry by ID'),
    )
)
