from datetime import datetime
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


YIBIN_LAT = 28.7513
YIBIN_LON = 104.6417


def get_time() -> str:
    time = datetime.now()
    return time.strftime("当前时间：%Y年%m月%d日 %H:%M:%S")


def get_yibin_today_weather() -> str:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={YIBIN_LAT}&longitude={YIBIN_LON}"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min"
        "&current_weather=true&timezone=Asia%2FShanghai"
    )
    try:
        data = _fetch_json(url)
    except (HTTPError, URLError, TimeoutError) as exc:
        return f"获取宜宾天气失败: {exc}"

    daily = data.get("daily", {})
    current = data.get("current_weather", {})

    date_list = daily.get("time", [])
    max_list = daily.get("temperature_2m_max", [])
    min_list = daily.get("temperature_2m_min", [])
    code_list = daily.get("weathercode", [])

    if not (date_list and max_list and min_list and code_list):
        return "未获取到完整的宜宾天气数据"

    weather_text = _weather_code_to_text(code_list[0])
    current_temp = current.get("temperature")
    current_part = f"，当前{current_temp}°C" if current_temp is not None else ""

    return (
        f"宜宾 {date_list[0]} 天气: {weather_text}"
        f"，最低{min_list[0]}°C，最高{max_list[0]}°C{current_part}"
    )


def get_yibin_today_air_quality() -> str:
    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={YIBIN_LAT}&longitude={YIBIN_LON}"
        "&hourly=us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
        "&timezone=Asia%2FShanghai"
    )
    try:
        data = _fetch_json(url)
    except (HTTPError, URLError, TimeoutError) as exc:
        return f"获取宜宾空气质量失败: {exc}"

    hourly = data.get("hourly", {})
    time_list = hourly.get("time", [])
    aqi_list = hourly.get("us_aqi", [])
    pm10_list = hourly.get("pm10", [])
    pm25_list = hourly.get("pm2_5", [])

    if not (time_list and aqi_list):
        return "未获取到完整的宜宾空气质量数据"

    index = _latest_today_available_index(time_list, aqi_list)
    if index is None:
        return "未获取到当日可用的宜宾 AQI 数据"

    aqi = aqi_list[index]
    pm10 = _format_optional_value(pm10_list, index, "PM10")
    pm25 = _format_optional_value(pm25_list, index, "PM2.5")
    extra_values = [value for value in (pm25, pm10) if value]
    extra = "，" + "，".join(extra_values) if extra_values else ""

    return f"宜宾 {time_list[index]} 空气质量: AQI {aqi}（{_aqi_level(aqi)}）{extra}"


def _fetch_json(url: str) -> dict:
    with urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def _latest_today_available_index(time_list: list, values: list) -> int | None:
    today = datetime.now().strftime("%Y-%m-%d")
    last_today_index = None
    for index, time_text in enumerate(time_list):
        if not str(time_text).startswith(today):
            continue
        if index < len(values) and values[index] is not None:
            last_today_index = index
    return last_today_index


def _format_optional_value(values: list, index: int, label: str) -> str:
    if index >= len(values) or values[index] is None:
        return ""
    return f"{label} {values[index]}ug/m3"


def _aqi_level(aqi: int | float) -> str:
    if aqi <= 50:
        return "优"
    if aqi <= 100:
        return "良"
    if aqi <= 150:
        return "轻度污染"
    if aqi <= 200:
        return "中度污染"
    if aqi <= 300:
        return "重度污染"
    return "严重污染"


def _weather_code_to_text(code: int) -> str:
    mapping = {
        0: "晴",
        1: "大部晴朗",
        2: "多云",
        3: "阴",
        45: "雾",
        48: "冻雾",
        51: "小毛毛雨",
        53: "毛毛雨",
        55: "大毛毛雨",
        56: "小冻毛毛雨",
        57: "大冻毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        66: "小冻雨",
        67: "大冻雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "小阵雨",
        81: "中阵雨",
        82: "大阵雨",
        85: "小阵雪",
        86: "大阵雪",
        95: "雷阵雨",
        96: "雷阵雨伴小冰雹",
        99: "雷阵雨伴大冰雹",
    }
    return mapping.get(code, f"未知天气代码({code})")

