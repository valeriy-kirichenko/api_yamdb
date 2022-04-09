from rest_framework import viewsets, mixins


class CreateListDestroyModelMixinSet(mixins.CreateModelMixin,
                                     mixins.ListModelMixin,
                                     mixins.DestroyModelMixin,
                                     viewsets.GenericViewSet):
    pass
