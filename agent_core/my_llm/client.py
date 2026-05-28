import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class LLMClient:
    def __init__(self, provider=None):
        self.provider = provider or os.getenv("PROVIDER", "deepseek")

        if self.provider == "deepseek":
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.base_url = os.getenv("DEEPSEEK_BASE_URL")
            self.model = os.getenv("DEEPSEEK_MODEL")
        elif self.provider == "zhipu":
            self.api_key = os.getenv("ZHIPU_API_KEY")
            self.base_url = os.getenv("ZHIPU_BASE_URL")
            self.model = os.getenv("ZHIPU_MODEL")
        else:
            raise ValueError(f"不支持的 provider: {self.provider}，请选择 deepseek 或 zhipu")

        if not self.api_key:
            raise ValueError(f"缺少 {self.provider.upper()}_API_KEY，请检查 .env 文件")
        if not self.base_url:
            raise ValueError(f"缺少 {self.provider.upper()}_BASE_URL，请检查 .env 文件")
        if not self.model:
            raise ValueError(f"缺少 {self.provider.upper()}_MODEL，请检查 .env 文件")

    def chat(self, messages, temperature=0.7):
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise Exception(f"API 错误 ({self.provider}): {exc.code} - {detail}") from exc
        except URLError as exc:
            raise Exception(f"API 请求失败 ({self.provider}): {exc}") from exc

        return data["choices"][0]["message"]["content"]


def load_env(path=".env"):
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = _strip_inline_comment(value.strip()).strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _strip_inline_comment(value: str) -> str:
    in_quote = False
    quote_char = ""
    for index, char in enumerate(value):
        if char in ['"', "'"]:
            if in_quote and char == quote_char:
                in_quote = False
            elif not in_quote:
                in_quote = True
                quote_char = char
        if char == "#" and not in_quote:
            return value[:index]
    return value


load_env()