import os
import requests
from requests.exceptions import RequestException
from procom.helpers import formalize, raise_requests_exception

API = os.environ.get("PROCOM_API", "https://procom-tracker.herokuapp.com/api")

# todo make sure to set function to correct url use regex clean // except http://


class ServiceAPI:
    """Service Api, push data to remote server"""

    @staticmethod
    def post(url: str, data: dict, timeout: int = 15) -> tuple:
        """Post data if not exist

        return True if created else False, along with the response object
        """
        try:
            response = requests.post(url, data=data, timeout=timeout)
            if response.status_code == 201:
                return True, response
        except RequestException as e:
            print("POST Exception, due to:", e)

        return False, response

    @staticmethod
    def put(
        url: str, reference: str, data: dict, files: dict = None, timeout: int = 15
    ) -> tuple:
        """Post data if not exist

        return True if created else False, along with the response object
        """

        try:
            response = requests.put(
                f"{url}{reference}/", data=data, files=files, timeout=timeout
            )
            if response.status_code == 200:
                return True, response

        except Exception as e:
            print("PUT Exception, due to:", e)

        return False, response

    @staticmethod
    def save(
        url: str,
        path: str,
        reference: str,
        data: dict,
        files: dict = None,
        timeout: int = 15,
    ) -> tuple:
        """Save data with both post and put

        requests issue with post data and file request
        - first we put data
        - if there is no data we create one, then we push the files if exist
        """

        url_path = f"{url}/{path}/"

        # try to put data
        saved, response = ServiceAPI.put(
            url=url_path, reference=reference, data=data, files=files, timeout=timeout
        )

        if saved:
            return response

        saved, response = ServiceAPI.post(url=url_path, data=data, timeout=timeout)
        if saved:
            if files:
                # if saved send files with data (issue with request post with files)
                saved, response = ServiceAPI.put(
                    url=url_path,
                    reference=reference,
                    data=data,
                    files=files,
                    timeout=timeout,
                )
            return response

        raise_requests_exception(response)


class ProductServiceAPI:
    """Specific APi for product"""

    @staticmethod
    def format(product: dict) -> tuple:
        """Format Product instantance

        return reference to correct forme, ex: 1/0 -> 1_0
        """
        reference = formalize(product["reference"])
        product["reference"] = reference
        return reference, product

    @staticmethod
    def prepare_file(filename: str, path: str = "output"):
        """Get file with binary read by filename"""
        try:
            return open(f"{path}/{filename}", "rb")
        except FileNotFoundError as e:
            print("Prepare File Exception, due to:", e)
            return None

    @staticmethod
    def prepare_files(files: dict, path: str = "output"):
        """Prepare a list of files"""
        result = {}
        if not files:
            return None
        for attribute, filename in files.items():
            file = ProductServiceAPI.prepare_file(filename, path)
            if file is None:
                continue
            result[attribute] = file

        return result

    @staticmethod
    def save(path: str, instance: dict, filenames: dict = None) -> None:
        """Specific save methd for product instance"""

        if not API:
            raise Exception("Specify your API Url in your Environment")
        try:
            # get formated data
            reference, product = ProductServiceAPI.format(instance)
            # set files
            files = ProductServiceAPI.prepare_files(filenames)
            # save data, files to remote service
            ServiceAPI.save(
                url=API, path=path, reference=reference, data=product, files=files
            )
        except Exception as e:
            print("<ProductServiceApi.Save>, Exception due to:", e)
