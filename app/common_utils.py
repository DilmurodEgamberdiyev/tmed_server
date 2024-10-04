from functools import partial

import grpc
from google.protobuf.json_format import MessageToDict
from rest_framework.exceptions import ValidationError


class BaseModelGRPCClient:
    def __init__(self, model_name: str, model_pb2, model_pb2_grpc, channel):
        self.model_name = model_name
        self.model_pb2 = model_pb2
        self.model_pb2_grpc = model_pb2_grpc
        stub_class = getattr(model_pb2_grpc, f'{self.model_name}ControllerStub')
        self.stub = stub_class(channel)
        self.retrieve_message_request = getattr(self.model_pb2, f'{self.model_name}RetrieveRequest', None)
        self.list_message_request = getattr(self.model_pb2, f'{self.model_name}ListRequest', None)
        self.model_message = getattr(self.model_pb2, self.model_name, None)

    def __getattr__(self, attr):
        return partial(self._wrapped_call, self.stub, attr)

    @staticmethod
    def _wrapped_call(*args, **kwargs):
        try:
            return getattr(args[0], args[1])(
                args[2], timeout=1000, **kwargs
            )
        except grpc.RpcError as e:
            print('Call {0} failed with {1}'.format(
                args[1], e)
            )
            raise


class ModelGRPCClient(BaseModelGRPCClient):

    def retrieve(self, **kwargs):
        if not self.retrieve_message_request:
            raise AttributeError('retrieve_message_request is None')
        func = getattr(self, 'Retrieve')
        response = func(self.retrieve_message_request(**kwargs))
        return MessageToDict(response)

    def list(self, **kwargs):
        if not self.list_message_request:
            raise AttributeError('list_message_request is None')
        func = getattr(self, 'List')
        response = func(self.list_message_request(**kwargs))
        return [MessageToDict(r) for r in response]

    def create(self, **kwargs):
        if not self.model_message:
            raise AttributeError('model_message is None')
        func = getattr(self, 'Create')
        response = func(self.model_message(**kwargs))
        return MessageToDict(response)

    def update(self, **kwargs):
        if not self.model_message:
            raise AttributeError('model_message is None')
        func = getattr(self, 'Update')
        response = func(self.model_message(**kwargs))
        return MessageToDict(response)

    def destroy(self, **kwargs):
        if not self.model_message:
            raise AttributeError('model_message is None')
        func = getattr(self, 'Destroy')
        response = func(self.model_message(**kwargs))
        return MessageToDict(response)


def rpc_error_to_validation_error(func):
    def _innner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as _exp:
            raise ValidationError({'message': str(_exp._state.details)})

    return _innner
