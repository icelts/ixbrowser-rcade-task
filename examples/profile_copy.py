import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Profile, Proxy, Preference, Fingerprint, Consts
from getproxy_wwp import get_proxy_ip

c = IXBrowserClient()
c.show_request_log = True

profile_id = 49
name = 'rcade' + str(int(time.time()))
site_id = Consts.DEFAULT_SITE_ID_BLANK_PAGE

result = c.create_profile_by_copying(profile_id, name, site_id=site_id)
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Create Profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'result:', result)

