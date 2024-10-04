from google.protobuf.json_format import MessageToDict

from common_utils import ModelGRPCClient, rpc_error_to_validation_error


class SpecialistModelGRPCClient(ModelGRPCClient):

    def list_specialist_detailed(self, **kwargs):
        func = getattr(self, 'ListSpecialistsDetailed')
        response = func(self.model_pb2.SpecialistListRequest(**kwargs))
        return [MessageToDict(r) for r in response]

    @rpc_error_to_validation_error
    def validate_meet_date(self, responsible, meet_time, duration):
        func = getattr(self, 'ValidateMeetDate')
        response = func(self.model_pb2.ValidateMeetDateRequest(
            specialist=int(responsible), meet_time=str(meet_time),
            duration=duration
        ))
        return MessageToDict(response)


class OrganizationModelGRPCClient(ModelGRPCClient):

    def organization_list_by_slug_name_list(self, **kwargs):
        func = getattr(self, 'OrganizationListBySlug')
        response = func(self.model_pb2.OrganizationSlugListRequest(**kwargs))
        return [MessageToDict(r) for r in response]

    @rpc_error_to_validation_error
    def retrieve(self, **kwargs):
        if not self.retrieve_message_request:
            raise AttributeError('retrieve_message_request is None')
        func = getattr(self, 'Retrieve')
        response = func(self.retrieve_message_request(**kwargs))
        return MessageToDict(response, preserving_proto_field_name=True)

    @rpc_error_to_validation_error
    def list(self, *args, **kwargs):
        if not self.list_message_request:
            raise AttributeError('list_message_request is None')
        func = getattr(self, 'List')
        response = func(self.list_message_request(**kwargs))
        return [MessageToDict(r, preserving_proto_field_name=True) for r in response]


class ProductToOrganizationModelGRPCClient(ModelGRPCClient):

    @rpc_error_to_validation_error
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @rpc_error_to_validation_error
    def set_remains_product(self, data: list):
        func = getattr(self, 'SetRemainsProduct')
        response = func(self.model_pb2.SetRemainsProductRequest(data=data))
        return MessageToDict(response)

    @rpc_error_to_validation_error
    def return_remains_product(self, data: dict):
        func = getattr(self, 'ReturnRemainsProduct')
        response = func(self.model_pb2.ReturnRemainsProductRequest(**data))
        return MessageToDict(response)

    def product_find(self, *args, **kwargs):
        func = getattr(self, 'ProductFind')
        response = func(self.model_pb2.ProductIdRequest(**kwargs))
        return [MessageToDict(r) for r in response]

    def list_consumables(self, *args, **kwargs):
        try:
            func = getattr(self, 'ListDependentProduct')
            response = func(self.model_pb2.DependentProductListRequest(**kwargs))
            result = [MessageToDict(r, preserving_proto_field_name=True) for r in response]
            return result
        except Exception as e:
            print(e)
            return []
