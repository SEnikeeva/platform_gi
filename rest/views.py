from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .readers.coords_reader import read_coords
from .readers.eor_reader import read_eor_prod, read_eor_inj
from .readers.isotopy_reader import read_isotopy
from .readers.micro_macro_reader import read_micro_macro
from .readers.mineralization_reader import read_mineralization
from .readers.perf_reader import read_perfs
from .readers.prc_reader import read_prc
from .readers.pressure_reader import read_pressure
from .readers.six_components_reader import read_six_components
from .readers.water_analysis_reader import read_water_analysis
from .readers.wc_reason_reader import read_wc_reason
from .readers.work_reader import read_works
from .serializers import *
from .submodels.diff_models import *
from .util import get_well_id, get_oil_deposit_id


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Project.objects.prefetch_related(
            Prefetch(
                'oil_deposits',
                queryset=OilDeposit.objects.all()
            )
        ).filter(company=company)


class OilDepositViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OilDepositSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return OilDeposit.objects.prefetch_related(
            Prefetch(
                'wells',
                queryset=Well.objects.all()
            )
        ).filter(company=company)


class WellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Well.objects.all()
    serializer_class = WellSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'oil_deposit', 'name'
    )

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Well.objects.filter(company=company)


class CoordsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CoordsSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        project = self.request.query_params.get('project')
        if project is None:
            return Coords.objects.filter(Q(company=company) & Q(project=None))
        else:
            coords_diff = CoordsDiff.objects.filter(project=project)
            origin_ids = [el['origin_id'] for el in coords_diff.values('origin_id')]
            coords = Coords.objects.filter(Q(company=company) & (Q(project=project) | Q(project=None)))\
                .exclude(id__in=origin_ids)
            return coords

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        coords_dict = read_coords(file)
        coords_list = []
        for el in coords_dict:
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            coords_list.append(Coords(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el
            ))
            if not one_oil_deposit:
                oil_deposit = None
        Coords.objects.bulk_create(coords_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class PerforationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PerforationSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Perforation.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        perf_ints = read_perfs(file)
        perf_ints_list = []
        for well_name, perf_data in perf_ints.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(perf_data) == 0) or (perf_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=perf_data[0].get('field'), company_id=company)
            well_id = get_well_id(well_name, oil_deposit_id=oil_deposit)
            for perf_int in perf_data:
                if perf_int.get('field') is not None:
                    del perf_int['field']
                perf_ints_list.append(Perforation(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **perf_int
                ))
            if not one_oil_deposit:
                oil_deposit = None
        Perforation.objects.bulk_create(perf_ints_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class EORProdViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EORPRodSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return EORProd.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        unit = request.data["unit"]
        company = request.data.get("company")

        eor_prod = read_eor_prod(file, unit=unit)
        eor_prod_list = []
        for well_name, eor_data in eor_prod.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(eor_data) == 0) or (eor_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=eor_data[0].get('field'), company_id=company)
            well_id = get_well_id(well_name, oil_deposit)
            for ed in eor_data:
                if ed.get('field') is not None:
                    del ed['field']
                eor_prod_list.append(EORProd(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **ed
                ))
            if not one_oil_deposit:
                oil_deposit = None
        EORProd.objects.bulk_create(eor_prod_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class EORInjViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EORInjSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return EORInj.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        eor_inj = read_eor_inj(file)
        eor_inj_list = []
        for well_name, eor_data in eor_inj.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(eor_data) == 0) or (eor_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=eor_data[0].get('field'), company_id=company)
            well_id = get_well_id(well_name, oil_deposit)
            for ed in eor_data:
                if ed.get('field') is not None:
                    del ed['field']
                eor_inj_list.append(EORInj(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **ed
                ))
            if not one_oil_deposit:
                oil_deposit = None
        EORInj.objects.bulk_create(eor_inj_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class MineralizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MineralizationSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Mineralization.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        mineralization_dict = read_mineralization(file)
        mineralization_list = []
        for el in mineralization_dict:
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            mineralization_list.append(Mineralization(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el
            ))
            if not one_oil_deposit:
                oil_deposit = None
        Mineralization.objects.bulk_create(mineralization_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class WCReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WCReasonSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return WCReason.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        wc_reason_dict = read_wc_reason(file)
        wc_reason_list = []
        for el in wc_reason_dict:
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            wc_reason_list.append(WCReason(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el
            ))
            if not one_oil_deposit:
                oil_deposit = None
        WCReason.objects.bulk_create(wc_reason_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class PressureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PressureSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Pressure.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        pressure_dict = read_pressure(file)
        pressure_list = []
        for well_name, pressure_data in pressure_dict.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(pressure_data) == 0) or (pressure_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=pressure_data[0].get('field'), company_id=company)
            well_id = get_well_id(well_name, oil_deposit)
            for pd in pressure_data:
                if pd.get('field') is not None:
                    del pd['field']
                pressure_list.append(Pressure(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **pd
                ))
            if not one_oil_deposit:
                oil_deposit = None
        Pressure.objects.bulk_create(pressure_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class WorkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Work.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        work_dict = read_works(file)
        work_list = []
        for well_name, work_data in work_dict.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(work_data) == 0) or (work_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=work_data[0].get('field'), company_id=company)
            well_id = get_well_id(well_name, oil_deposit)
            for wd in work_data:
                if wd.get('field') is not None:
                    del wd['field']
                work_list.append(Work(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **wd
                ))
            if not one_oil_deposit:
                oil_deposit = None
        Work.objects.bulk_create(work_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class PressureRecoveryCurveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PressureRecoveryCurveSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return PressureRecoveryCurve.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        prc_dict = read_prc(file)
        prc_list = []
        for well_name, prc_data in prc_dict.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(prc_data) == 0) or (prc_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=prc_data[0].get('field'), company_id=company)
            well_id = get_well_id(well_name, oil_deposit)
            for wd in prc_data:
                if wd.get('field') is not None:
                    del wd['field']
                prc_list.append(PressureRecoveryCurve(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **wd
                ))
            if not one_oil_deposit:
                oil_deposit = None
        PressureRecoveryCurve.objects.bulk_create(prc_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class WaterAnalysisViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WaterAnalysisSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return WaterAnalysis.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        water_analysis_dict = read_water_analysis(file)
        water_analysis_list = []
        for well_name, water_analysis_data in water_analysis_dict.items():
            if oil_deposit is None:
                one_oil_deposit = False
                if (len(water_analysis_data) == 0) or (water_analysis_data[0].get('field') is None):
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=water_analysis_data[0].get('field'),
                                                     company_id=company)
            well_id = get_well_id(well_name, oil_deposit)
            for wd in water_analysis_data:
                if wd.get('field') is not None:
                    del wd['field']
                water_analysis_list.append(WaterAnalysis(
                    well_id=well_id,
                    oil_deposit_id=oil_deposit,
                    company_id=company,
                    **wd
                ))
            if not one_oil_deposit:
                oil_deposit = None
        WaterAnalysis.objects.bulk_create(water_analysis_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class IsotopyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IsotopySerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return Isotopy.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        isotopy_dict = read_isotopy(file)
        isotopy_list = []
        for el in isotopy_dict:
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            isotopy_list.append(Isotopy(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el
            ))
            if not one_oil_deposit:
                oil_deposit = None
        Isotopy.objects.bulk_create(isotopy_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class WaterMicroMacroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WaterMicroMacroSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return WaterMicroMacro.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        water_micro_macro_dict, components_dict = read_micro_macro(file)
        water_micro_macro_list = []
        for el, comps in zip(water_micro_macro_dict, components_dict):
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            water_micro_macro_list.append(WaterMicroMacro(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el,
                components=comps
            ))
            if not one_oil_deposit:
                oil_deposit = None
        WaterMicroMacro.objects.bulk_create(water_micro_macro_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class OilMicroMacroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OilMicroMacroSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return OilMicroMacro.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        oil_micro_macro_dict, components_dict = read_micro_macro(file)
        oil_micro_macro_list = []
        for el, comps in zip(oil_micro_macro_dict, components_dict):
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            oil_micro_macro_list.append(OilMicroMacro(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el,
                components=comps
            ))
            if not one_oil_deposit:
                oil_deposit = None
        OilMicroMacro.objects.bulk_create(oil_micro_macro_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class SixComponentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SixComponentsSerializer

    def get_queryset(self):
        company = self.request.query_params.get('company')
        return SixComponents.objects.filter(company=company)

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        oil_deposit = request.data.get("oil_deposit")
        one_oil_deposit = True
        company = request.data.get("company")

        six_components_dict, anions_dict, cations_dict = read_six_components(file)
        six_components_list = []
        for el, anions, cations in zip(six_components_dict, anions_dict, cations_dict):
            if oil_deposit is None:
                one_oil_deposit = False
                if el.get('field') is None:
                    continue
                else:
                    oil_deposit = get_oil_deposit_id(oil_deposit_name=el.get('field'), company_id=company)
                    del el['field']
            well_id = get_well_id(el['well'], oil_deposit)
            del el['well']
            six_components_list.append(SixComponents(
                well_id=well_id,
                oil_deposit_id=oil_deposit,
                company_id=company,
                **el,
                anions=anions,
                cations=cations
            ))
            if not one_oil_deposit:
                oil_deposit = None
        SixComponents.objects.bulk_create(six_components_list)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)
