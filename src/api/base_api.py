import requests
import logging 
import time

logger = logging.getLogger(__name__)

class BaseAPI:
    def __init__(self, base_url, timeout = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method, endpoint, params=None, headers=None):
        
        url = f"{self.base_url}/{endpoint}" 
        start_time = time.time()
        response_time = None

        try:
            response = self.session.request(
                method = method,
                url = url,
                params = params,
                headers=headers,
                timeout=self.timeout
            )    

            response_time = time.time() - start_time 
            logger.info(
                "API request,  method: %s, url: %s, params: %s time: %s", 
                 method, url, params, response_time
            )

            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time 
            
            logger.error(
                "API request,  method: %s, url: %s, params: %s time: %s, error: %s",
                 method, url, params, response_time, e)
            raise 
           