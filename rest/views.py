from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.decorators import action

from .readers.coords_reader import read_coords
from .readers.eor_reader import read_eor_prod, read_eor_inj
from .readers.mineralization_reader import read_mineralization
from .readers.perf_reader import read_perfs
from .readers.pressure_reader import read_pressure
from .readers.wc_reason_reader import read_wc_reason
from .serializers import *
from .util import get_well_id


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
            well_id = get_well_id(el['well'], oil_deposit)
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
            well_id = get_well_id(well_name, oil_deposit_id=oil_deposit)
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


class EORProdViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EORPRodSerializer

    def get_queryset(self):
        return EORProd.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]
        unit = request.data["unit"]

        eor_prod = read_eor_prod(file, unit=unit)
        eor_prod_list = []
        for well_name, eor_data in eor_prod.items():
            well_id = get_well_id(well_name, oil_deposit)
            for ed in eor_data:
                eor_prod_list.append(EORProd(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    date=ed.get('date'),
                    level=ed.get('level'),
                    layer=ed.get('layer'),
                    work_hours=ed.get('work_hours'),
                    q_oil=ed.get('q_oil'),
                    q_water=ed.get('q_water'),
                    fluid_rate=ed.get('fluid_rate'),
                    sgw=ed.get('sgw')
                ))
        EORProd.objects.bulk_create(eor_prod_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class EORInjViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EORInjSerializer

    def get_queryset(self):
        return EORInj.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]

        eor_inj = read_eor_inj(file)
        eor_inj_list = []
        for well_name, eor_data in eor_inj.items():
            well_id = get_well_id(well_name, oil_deposit)
            for ed in eor_data:
                eor_inj_list.append(EORInj(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    date=ed.get('date'),
                    level=ed.get('level'),
                    layer=ed.get('layer'),
                    work_hours=ed.get('work_hours'),
                    q_water3=ed.get('q_water3'),
                    acceleration=ed.get('acceleration'),
                    agent_code=ed.get('agent_code'),
                ))
        EORInj.objects.bulk_create(eor_inj_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class MineralizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MineralizationSerializer

    def get_queryset(self):
        return Mineralization.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]

        mineralization_dict = read_mineralization(file)
        mineralization_list = []
        for el in mineralization_dict:
            well_id = get_well_id(el['well'], oil_deposit)
            mineralization_list.append(Mineralization(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    start_date=el.get('start'),
                    end_date=el.get('end'),
                    type=el.get('type'),
            ))
        Mineralization.objects.bulk_create(mineralization_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class WCReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WCReasonSerializer

    def get_queryset(self):
        return WCReason.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]

        wc_reason_dict = read_wc_reason(file)
        wc_reason_list = []
        for el in wc_reason_dict:
            well_id = get_well_id(el['well'], oil_deposit)
            wc_reason_list.append(WCReason(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    date=el.get('date'),
                    category=el.get('category'),
                    type=el.get('type'),
            ))
        WCReason.objects.bulk_create(wc_reason_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class PressureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PressureSerializer

    def get_queryset(self):
        return Pressure.objects.filter(author=self.request.user)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data["oil_deposit"]

        pressure_dict = read_pressure(file)
        pressure_list = []
        for well_name, pressure_data in pressure_dict.items():
            well_id = get_well_id(well_name, oil_deposit)
            for pd in pressure_data:
                pressure_list.append(Pressure(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    date=pd.get('date'),
                    type=pd.get('type'),
                    pressure=pd.get('pressure')
                ))
        Pressure.objects.bulk_create(pressure_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)
