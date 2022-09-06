from rest_framework import viewsets, mixins


class CreateListDestroyModelMixinSet(mixins.CreateModelMixin,
                                     mixins.ListModelMixin,
                                     mixins.DestroyModelMixin,
                                     viewsets.GenericViewSet):
    """Класс примесь для создания, вывода списка, удаления объектов"""

    pass
