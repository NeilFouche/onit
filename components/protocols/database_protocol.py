from typing import Protocol, Optional
from components.graphs.graph import Graph
from components.sources.databases import Table

from components.protocols.logentry_protocol import LogEntryTable
from components.protocols.session_protocol import SessionTable
from components.protocols.permission_protocol import PermissionTable
from components.protocols.group_protocol import GroupTable
from components.protocols.user_protocol import UserTable
from components.protocols.contenttype_protocol import ContentTypeTable
from components.protocols.feature_protocol import FeatureTable
from components.protocols.reportingstructure_protocol import ReportingStructureTable
from components.protocols.functionalarea_protocol import FunctionalAreaTable
from components.protocols.region_protocol import RegionTable
from components.protocols.parameter_protocol import ParameterTable
from components.protocols.terminology_protocol import TerminologyTable
from components.protocols.mediaasset_protocol import MediaAssetTable
from components.protocols.service_protocol import ServiceTable
from components.protocols.servicemethod_protocol import ServiceMethodTable
from components.protocols.office_protocol import OfficeTable
from components.protocols.operatinghours_protocol import OperatingHoursTable
from components.protocols.equipment_protocol import EquipmentTable
from components.protocols.faq_protocol import FaqTable
from components.protocols.segment_protocol import SegmentTable
from components.protocols.body_protocol import BodyTable
from components.protocols.bodyitem_protocol import BodyItemTable
from components.protocols.enquiry_protocol import EnquiryTable
from components.protocols.role_protocol import RoleTable
from components.protocols.person_protocol import PersonTable
from components.protocols.employee_protocol import EmployeeTable
from components.protocols.page_protocol import PageTable
from components.protocols.socialplatform_protocol import SocialPlatformTable
from components.protocols.entityfeature_protocol import EntityFeatureTable
from components.protocols.entitymedia_protocol import EntityMediaTable

class RelationalDatabase(Protocol):
    log_entry: LogEntryTable
    session: SessionTable
    permission: PermissionTable
    group: GroupTable
    user: UserTable
    content_type: ContentTypeTable
    feature: FeatureTable
    reporting_structure: ReportingStructureTable
    functional_area: FunctionalAreaTable
    region: RegionTable
    parameter: ParameterTable
    terminology: TerminologyTable
    media_asset: MediaAssetTable
    service: ServiceTable
    service_method: ServiceMethodTable
    office: OfficeTable
    operating_hours: OperatingHoursTable
    equipment: EquipmentTable
    faq: FaqTable
    segment: SegmentTable
    body: BodyTable
    body_item: BodyItemTable
    enquiry: EnquiryTable
    role: RoleTable
    person: PersonTable
    employee: EmployeeTable
    page: PageTable
    social_platform: SocialPlatformTable
    entity_feature: EntityFeatureTable
    entity_media: EntityMediaTable

    def get(self, table_name: Optional[str] = None, model_name: Optional[str] = None, content_type_id: Optional[int] = None) -> Table: ...

    @property
    def table_names(self) -> list[str]: ...

    @property
    def name(self) -> str: ...

    @property
    def schema(self) -> dict: ...

    @property
    def schema_graph(self) -> Graph: ...
