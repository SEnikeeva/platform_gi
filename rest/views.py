from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.decorators import action

from .readers.coords_reader import read_coords
from .readers.perf_reader import read_perfs
from .serializers import *


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related(
            Prefetch(
                'oil_deposits',
                queryset=OilDeposit.objects.all()
            )
        ).filter(author=self.request.user)


class OilDepositViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OilDepositSerializer

    def get_queryset(self):
        return OilDeposit.objects.prefetch_related(
            Prefetch(
                'wells',
                queryset=Well.objects.all()
            )
        ).filter(author=self.request.user)


class WellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WellSerializer

    def get_queryset(self):
        return Well.objects.filter(author=self.request.user)


class CoordsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CoordsSerializer

    def get_queryset(self):
        return Coords.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]

        coords_dict = read_coords(file)
        coords_list = []
        for el in coords_dict:
            well_name = el['well']
            well = Well.objects.filter(name=well_name).all()
            if len(well) == 0:
                new_well = Well.objects.create(
                    oil_deposit_id=oil_deposit,
                    name=well_name,
                )
                well_id = new_well.id
            else:
                well_id = well[0].id
            coords_list.append(Coords(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                x=el.get('x'),
                y=el.get('y'),
                level=el.get('level'),
                layer=el.get('layer')
            ))
        Coords.objects.bulk_create(coords_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class PerforationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PerforationSerializer

    def get_queryset(self):
        return Perforation.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]

        perf_ints = read_perfs(file)
        perf_ints_list = []
        for well_name, perf_data in perf_ints.items():
            well = Well.objects.filter(name=well_name).all()
            if len(well) == 0:
                new_well = Well.objects.create(
                    oil_deposit_id=oil_deposit,
                    name=well_name,
                )
                well_id = new_well.id
            else:
                well_id = well[0].id
            for perf_int in perf_data:
                perf_ints_list.append(Perforation(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    top=perf_int.get('top'),
                    bot=perf_int.get('bot'),
                    layer=perf_int.get('layer'),
                    perf_type=perf_int.get('type'),
                    date=perf_int.get('date')
                ))
        Perforation.objects.bulk_create(perf_ints_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)
