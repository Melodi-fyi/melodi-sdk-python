from logging import Logger

from requests import Response


def _log_melodi_http_errors(logger: Logger, response: Response):
    if (response.status_code == 400):
        try:
            responseJson = response.json()
            if ("errors" in responseJson):
                for error in responseJson["errors"]:
                    logger.error(f"Bad Request response from Melodi API: {error}")
            else:
                logger.error(f"Bad Request response from Melodi API: {responseJson}")
        except:
            pass