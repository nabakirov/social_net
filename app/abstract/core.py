import typing as t

import requests
import json

from . import exceptions as exc
from . import models as m


class AbstractRequests:
    session: requests.Session = None

    def __init__(self,
                 proxy: dict = None,
                 timeout: int = 10,
                 raise_exception: bool = True):
        """
        proxies: {'http': 'schema://user:password@host:port'}
        """
        self.session = requests.Session()

        if proxy:
            self.session.proxies.update(proxy)
        self.timeout = timeout
        self.raise_exception = raise_exception

    def get_request_log(self, **kwargs):
        # todo: add session info
        return json.dumps({
            'url': kwargs.pop('url', None),
            'query_params': kwargs.pop('query_params', None),
            'headers': kwargs.pop('headers', None),
            'data': kwargs
        })

    def _request(self, method, url, **kwargs):
        timeout = kwargs.pop('timeout', self.timeout)
        r = self.session.request(method=method, url=url, **kwargs, timeout=timeout)

        if r.status_code == 404:
            if self.raise_exception:
                raise exc.NotFound(detail=self.get_request_log(url=url, **kwargs,
                                                               received=r.text,
                                                               status_code=r.status_code))
        elif r.status_code == 401:
            if self.raise_exception:
                raise exc.Unauthorized(message='received 401',
                                       detail=self.get_request_log(url=url, **kwargs,
                                                                   received=r.text,
                                                                   status_code=r.status_code))
        elif r.status_code == 403:
            if self.raise_exception:
                raise exc.Forbidden(message='received 403',
                                    detail=self.get_request_log(url=url, **kwargs,
                                                                received=r.text,
                                                                status_code=r.status_code))
        elif r.status_code == 429:
            if self.raise_exception:
                raise exc.TooManyRequests(detail=self.get_request_log(url=url, **kwargs,
                                                                      received=r.text,
                                                                      status_code=r.status_code))

        elif not r.ok:
            if self.raise_exception:
                raise exc.InvalidResponse(message='Received non 200',
                                          detail=self.get_request_log(url=url, **kwargs,
                                                                      received=r.text,
                                                                      status_code=r.status_code))
        return r

    def get(self, url, **kwargs):
        return self._request(method='get', url=url, **kwargs)

    def post(self, url, **kwargs):
        return self._request(method='post', url=url, **kwargs)

    def patch(self, url, **kwargs):
        return self._request(method='patch', url=url, **kwargs)

    def put(self, url, **kwargs):
        return self._request(method='put', url=url, **kwargs)


class AbstractAPI:
    def __init__(self,
                 email_api_key: str = None,
                 ip_api_key: str = None,
                 holiday_api_key: str = None,
                 session: requests = None,
                 timeout: int = 10,
                 raise_exception: bool = True,
                 proxy: dict = None):
        self.email_api_key = email_api_key
        self.ip_api_key = ip_api_key
        self.holiday_api_key = holiday_api_key
        if session is None:
            self.session = AbstractRequests(
                timeout=timeout,
                raise_exception=raise_exception,
                proxy=proxy
            )
        else:
            self.session = session

    def get_headers(self):
        return {}

    def email_info(self, email: str) -> m.EmailValidation:
        assert self.email_api_key is not None, 'email_api_key is not set'
        url = 'https://emailvalidation.abstractapi.com/v1/'
        headers = self.get_headers()
        params = {
            'api_key': self.email_api_key,
            'email': email
        }
        r = self.session.get(url=url, headers=headers, params=params)
        return m.EmailValidation(**r.json())

    def ip_info(self, ip: str) -> m.LocationModel:
        assert self.ip_api_key is not None, 'ip_api_key is not set'
        url = 'https://ipgeolocation.abstractapi.com/v1/'
        headers = self.get_headers()
        params = {
            'api_key': self.ip_api_key,
            'ip_address': ip
        }
        r = self.session.get(url=url, headers=headers, params=params)
        return m.LocationModel(**r.json())

    def holiday_info(self,
                     country_code: str,
                     year: int = None,
                     month: int = None,
                     day: int = None) -> t.List[m.HolidayModel]:
        assert self.holiday_api_key is not None, 'holiday_api_key is not set'
        url = 'https://holidays.abstractapi.com/v1/'
        headers = self.get_headers()
        params = {
            'api_key': self.holiday_api_key,
            'country': country_code
        }
        if year is not None:
            params['year'] = year
        if month is not None:
            params['month'] = month
        if day is not None:
            params['day'] = day
        r = self.session.get(url=url, headers=headers, params=params)
        return [m.HolidayModel(**obj) for obj in r.json()]