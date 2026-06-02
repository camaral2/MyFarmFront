import requests
from flask import abort, session

class APIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token or session.get('user_token')

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _handle_response(self, response):
        if response.status_code == 401:
            abort(401)
        try:
            response.raise_for_status()
            if response.content:
                return response.json()
            return None
        except requests.exceptions.HTTPError as e:
            try:
                data = response.json()
                detail = data.get("detail")
                message = None
                if isinstance(detail, dict):
                    message = detail.get("message")
                elif isinstance(detail, list) and len(detail) > 0 and isinstance(detail[0], dict):
                    message = detail[0].get("message")
                raise RuntimeError(f"API Error: {message or str(detail)}")
            except Exception:
                print(f"Response content: {response.text}")
                raise RuntimeError(f"API request failed: {str(e)}") from e

    def _join_url(self, endpoint):
        base = self.base_url.rstrip('/')
        path = endpoint.lstrip('/')
        return f"{base}/{path}"

    def get(self, endpoint):
        try:
            print(f'api_client.get {endpoint}')
            url = self._join_url(endpoint)
            response = requests.get(url, headers=self._headers())
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}") from e
        except ValueError as e: # Catch JSON decode errors
            raise RuntimeError(f"API returned invalid JSON: {str(e)}") from e

    def post(self, endpoint, json=None):
        try:
            print(f'api_client.post {endpoint}')
            url = self._join_url(endpoint)
            response = requests.post(url, headers=self._headers(), json=json)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}") from e
        except ValueError as e:
            raise RuntimeError(f"API returned invalid JSON: {str(e)}") from e

    def put(self, endpoint, json=None):
        try:
            print(f'api_client.put {endpoint}')
            url = self._join_url(endpoint)
            response = requests.put(url, headers=self._headers(), json=json)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}") from e
        except ValueError as e:
            raise RuntimeError(f"API returned invalid JSON: {str(e)}") from e

    def delete(self, endpoint):
        try:
            print(f'api_client.delete {endpoint}')
            url = self._join_url(endpoint)
            response = requests.delete(url, headers=self._headers())
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}") from e
        except ValueError as e:
            raise RuntimeError(f"API returned invalid JSON: {str(e)}") from e
