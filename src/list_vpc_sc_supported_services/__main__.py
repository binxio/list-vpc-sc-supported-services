import re
import requests
import logging
from io import StringIO
from bs4 import BeautifulSoup


def scrape_vpc_service_controls_supported_products() -> dict:
    """
    scrapes the web page https://cloud.google.com/vpc-service-controls/docs/supported-products. The page
    describes which Google Cloud Platform services are supported and at which support level: ga, beta or preview.

    :return: dictionary with a list of service names per support level
    """
    page = requests.get(
        "https://cloud.google.com/vpc-service-controls/docs/supported-products"
    )

    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all("table", class_="supported-product-details")

    result = {}
    for table in tables:
        values = [r.get_text().strip() for r in table.find_all("td")]
        details = {values[i]: values[i + 1] for i in range(0, len(values), 2)}
        status = details.get("Status")
        service_name = details.get("Service name")
        if service_name and status:
            status = status.split(".", 1)[0]
            service_names = [
                re.sub(r"\s+(beta)?\s*", "", s) for s in re.split(r",", service_name)
            ]
            if status not in result:
                result[status] = set()
            result[status].update(service_names)
    return result


def remove_mixed_status(services: dict):
    """
    removes all services from Beta or Preview that are also in GA. generates a warning message
    """
    for service in services["GA"]:
        for status in services.keys():
            if status.upper() != "GA" and service in services[status]:
                logging.warning(
                    "service '%s' is available both in status GA as in status '%s', please check the documentation",
                    service,
                    status,
                )
                services[status].remove(service)


def generate_tf_variable(services: dict) -> str:

    """
    prints out a terraform style dictionary of string lists. The key is the status of the service in lowercase, the value
    an array of service names in that status.

    to use, type:
         hcledit attributes set locals.vpc_sc_services \
         "$(list-vpc-sc-supported-services)" \
         --file locals.tf \
         --update
    """
    result = StringIO()

    result.write("{\n")
    for status in sorted(services.keys()):
        result.write(f"  {status.lower()} = [\n")
        for n in sorted(services[status]):
            result.write(f'    "{n}",\n')
        result.write("  ]\n")
    result.write("}\n")
    return result.getvalue()


def main():
    services = scrape_vpc_service_controls_supported_products()
    remove_mixed_status(services)
    print(generate_tf_variable(services))


if __name__ == "__main__":
    main()
