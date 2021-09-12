#!/usr/bin/env python3

from .bbox_requests import BboxRequests
from .bbox_api_endpoints import BboxApiEndpoints

class Bbox(BboxRequests):
    def __init__(self, api_host: str=None, password: str=None) -> None:
        super().__init__(api_host, password)

    def get_bbox_info(self):
        return self.request(*BboxApiEndpoints.get_bbox_info).json()

    def set_display_luminosity(self, luminosity):
        assert luminosity in range(0, 101)
        return self.request(
            *BboxApiEndpoints.set_display_luminosity,
            data={'luminosity': luminosity}
        )

    def reboot(self):
        return self.request(*BboxApiEndpoints.reboot)

    def get_all_connected_devices(self):
        return self.request(*BboxApiEndpoints.get_all_connected_devices)['hosts']['list']

    def login(self):
        return self.do_auth()

    def logout(self):
        return self.request(*BboxApiEndpoints.logout)

    def get_ip_stats(self):
        return self.request(*BboxApiEndpoints.get_ip_stats)['wan']['ip']['stats']
