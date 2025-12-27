from checkin_pb2 import CheckinRequest, CheckinResponse
from build_prop_parser import BuildPropParser
import time
import random
from zoneinfo import ZoneInfo
import requests

def makeRequest_(props):
    FALLBACK = 'unknown'

    builder = CheckinRequest()

    build_data = builder.checkin.build
    build_data.brand = props.get('ro.product.system.brand', FALLBACK)
    build_data.bootloader = props.get('ro.bootloader', FALLBACK)
    build_data.clientId = 'android-google' # from GmsCore
    build_data.device = props.get('ro.product.system.device', FALLBACK)
    build_data.fingerprint = props.get('ro.system.build.fingerprint', FALLBACK)
    build_data.hardware = props.get('ro.hardware', FALLBACK)
    build_data.manufacturer = props.get('ro.product.system.manufacturer', FALLBACK)
    build_data.model = props.get('ro.product.system.model', FALLBACK)
    build_data.otaInstalled = False  # from GmsCore
    build_data.product = props.get('ro.build.product', FALLBACK)
    build_data.radio = props.get('?', FALLBACK) # idk
    build_data.sdkVersion = int(props.get('ro.system.build.version.sdk'))
    build_data.time = int(props.get('ro.build.date.utc', int(time.time()/1000))) # idk

    builder.checkin.cellOperator = 'kt' # idk. exmaple

    event_item = builder.checkin.event.add()
    event_item.tag = 'event_log_start' # main profile인 경우. 아니면 "system_update"
    event_item.value = '' # main profile인 경우. 아니면 "1536,0,-1,NULL"
    event_item.timeMs = int(time.time() * 1000) # ms int64 time

    builder.checkin.lastCheckinMs = 0
    # requestedGroup
    builder.checkin.roaming = "WIFI::" # "WIFI::" | ("mobile" | "notmobile" | "unknown") + "-" + ("roaming" | "notroaming" | "unknown")
    # imOperator
    # stat
    builder.checkin.userNumber = 0 # 상수?

    # deviceConfiguration
    builder.digest = "1-9599894992638872385" # Java: .digest(checkinInfo.getDigest()) 로직 없는 임의 값임.
    # esn
    builder.fragment = 0
    builder.locale = "ko_KR" # list에서 rand 뽑기 고려
    builder.loggingId = random.randint(-(2**63), 2**63 - 1) # 64bit signed long?
    builder.meid = 'ffffffffffffff' # 16 rand hex %x
    builder.otaCert.extend(['71Q6Rn2DDZl1zPDVaaeEHItd']) # 고정 키값 from GmsCore
    builder.timeZone = time.tzname[0]  # "KST" 형식임 "Asia/Seoul" 형식임???
    builder.userName = FALLBACK # null? unknown? idk
    builder.userSerialNumber = 0 # randint? idk
    builder.version = 3

    # 반복 필드인데 ㅁㄹ
    if not builder.accountCookie:
        builder.accountCookie.append("")

    # Build.SERIAL 대응?
    serial = props.get('ro.serialno')
    if serial:
        builder.serial = serial

    return builder.SerializeToString()

def req_(target):
    url = "https://android.clients.google.com/checkin"
    
    headers = {
        "Content-type": "application/x-protobuffer",
        "User-Agent": "Android-Checkin/2.0 (vbox86p JLS36G); gzip"
    }

    response = requests.post(url, headers=headers, data=target)

    return response.content

def getToken(path: str):
    parser = BuildPropParser(path)
    props = parser.parse()
    target = makeRequest_(props)
    resp = req_(target)
    checkin_resp = CheckinResponse()
    checkin_resp.ParseFromString(resp)
    return checkin_resp.androidId, checkin_resp.securityToken, props
