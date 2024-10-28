import typing as t
from pydantic import BaseModel


class ValueText(BaseModel):
    value: bool
    text: str


class EmailValidation(BaseModel):
    email: str
    autocorrect: t.Optional[str] = None
    deliverability: str
    quality_score: float
    is_valid_format: t.Optional[ValueText] = None
    is_free_email: t.Optional[ValueText] = None
    is_disposable_email: t.Optional[ValueText] = None
    is_role_email: t.Optional[ValueText] = None
    is_catchall_email: t.Optional[ValueText] = None
    is_mx_found: t.Optional[ValueText] = None
    is_smtp_valid: t.Optional[ValueText] = None


class SecurityModel(BaseModel):
    is_vpn: t.Optional[bool] = None


class TimezoneModel(BaseModel):
    name: t.Optional[str] = None
    abbreviation: t.Optional[str] = None
    gmt_offset: t.Optional[int] = None
    current_time: t.Optional[str] = None
    is_dst: t.Optional[bool] = None


class FlagModel(BaseModel):
    emoji: t.Optional[str] = None
    unicode: t.Optional[str] = None
    png: t.Optional[str] = None
    svg: t.Optional[str] = None


class CurrencyModel(BaseModel):
    currency_name: t.Optional[str] = None
    currency_code: t.Optional[str] = None


class ConnectionModel(BaseModel):
    autonomous_system_number: t.Optional[int] = None
    autonomous_system_organization: t.Optional[str] = None
    connection_type: t.Optional[str] = None
    isp_name: t.Optional[str] = None
    organization_name: t.Optional[str] = None


class LocationModel(BaseModel):
    ip_address: t.Optional[str] = None
    city: t.Optional[str] = None
    city_geoname_id: t.Optional[int] = None
    region: t.Optional[str] = None
    region_iso_code: t.Optional[str] = None
    region_geoname_id: t.Optional[int] = None
    postal_code: t.Optional[str] = None
    country: t.Optional[str] = None
    country_code: t.Optional[str] = None
    country_geoname_id: t.Optional[int] = None
    country_is_eu: t.Optional[bool] = None
    continent: t.Optional[str] = None
    continent_code: t.Optional[str] = None
    continent_geoname_id: t.Optional[int] = None
    longitude: t.Optional[float] = None
    latitude: t.Optional[float] = None
    security: t.Optional[SecurityModel] = None
    timezone: t.Optional[TimezoneModel] = None
    flag: t.Optional[FlagModel] = None
    currency: t.Optional[CurrencyModel] = None
    connection: t.Optional[ConnectionModel] = None


class HolidayModel(BaseModel):
    name: t.Optional[str] = None
    name_local: t.Optional[str] = None
    language: t.Optional[str] = None
    description: t.Optional[str] = None
    country: t.Optional[str] = None
    location: t.Optional[str] = None
    type: t.Optional[str] = None
    date: t.Optional[str] = None
    date_year: t.Optional[str] = None
    date_month: t.Optional[str] = None
    date_day: t.Optional[str] = None
    week_day: t.Optional[str] = None
