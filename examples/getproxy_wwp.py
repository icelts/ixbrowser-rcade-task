import requests
import time

def get_proxy_info(api_key, max_retries=6, retry_delay=25):
    """
    通过 API 请求获取代理信息。

    参数:
        api_key (str): API 的 key。
        max_retries (int): 最大重试次数，默认为 6 次。
        retry_delay (int): 每次重试的等待时间（秒），默认为 25 秒。

    返回:
        dict: 包含代理信息的字典，格式为 {"ip": "xxx.xxx.xxx.xxx", "port": xxxx}。
              如果失败，返回 None。
    """
    url = "https://wwproxy.com/api/client/proxy/available"
    params = {
        "key": api_key,
        "provinceId": -1
    }

    for attempt in range(max_retries):
        try:
            # 发送 API 请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查 HTTP 状态码

            # 解析返回的 JSON 数据
            result = response.json()

            # 检查请求状态
            if result.get("status") == "OK" and result.get("data") is not None:
                proxy_data = result["data"]
                return {
                    "ip": proxy_data["ipAddress"],
                    "port": proxy_data["port"]
                }
            else:
                print(f"请求失败: {result.get('message')}")

        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")

        # 如果未成功，等待一段时间后重试
        if attempt < max_retries - 1:
            print(f"等待 {retry_delay} 秒后重试... (剩余重试次数: {max_retries - attempt - 1})")
            time.sleep(retry_delay)

    # 重试次数用尽仍未成功
    print("重试次数用尽，未能获取代理信息。")
    return None

