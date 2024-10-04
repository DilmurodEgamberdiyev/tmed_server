from os import getenv

import grpc

from management.grpc_model_clients import OrganizationModelGRPCClient, SpecialistModelGRPCClient, \
    ProductToOrganizationModelGRPCClient
from management.grpc_protos import organization_pb2, organization_pb2_grpc, specialist_pb2, specialist_pb2_grpc
from management.grpc_protos.product_to_org import product_pb2, product_pb2_grpc
from root.settings import env


class BMSGRPCClient:
    def __init__(self):
        host = env.str('BMS_GRPC_HOST')
        port = env.int('BMS_GRPC_PORT')
        channel = grpc.insecure_channel('{0}:{1}'.format(host, port))
        self.organization = OrganizationModelGRPCClient(
            model_name='Organization', model_pb2=organization_pb2,
            model_pb2_grpc=organization_pb2_grpc, channel=channel
        )
        self.specialist = SpecialistModelGRPCClient(
            'Specialist', specialist_pb2, specialist_pb2_grpc, channel
        )


class PMSGRPCClient:
    def __init__(self):
        host = env.str('PMS_GRPC_HOST')
        port = env.int('PMS_GRPC_PORT')
        channel = grpc.insecure_channel('{0}:{1}'.format(host, port))
        self.product_to_org = ProductToOrganizationModelGRPCClient(
            'ProductToOrganization', product_pb2, product_pb2_grpc, channel
        )


bms_client = BMSGRPCClient()
pms_client = PMSGRPCClient()


# pms_client = PMSGRPCClient()


def get_service_client(name: str):
    services = {
        'BMS': bms_client,
        # 'PMS': pms_client,
    }
    return services[name.upper()]
