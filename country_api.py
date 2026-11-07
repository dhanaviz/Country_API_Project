
import requests
import re

API_URL = "https://countries.dev/name/{}"


def validate_country_name(country):
    country = country.strip()

    if not country:
        raise ValueError("Country name cannot be empty.")

    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", country):
        raise ValueError("Please enter a valid country name.")

    return country


def fetch_country_data(country):
    url = API_URL.format(requests.utils.quote(country))

    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 404:
            print("\nNo matching country found.")
            return None

        if response.status_code == 429:
            print("\nToo many requests. Try again later.")
            return None

        if response.status_code >= 500:
            print("\nAPI is currently unavailable.")
            return None

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout:
        print("\nNetwork timeout. Try again.")
        return None

    except requests.exceptions.ConnectionError:
        print("\nNetwork error. Check internet.")
        return None

    except requests.exceptions.HTTPError:
        print("\nAPI request failed.")
        return None

    except requests.exceptions.RequestException:
        print("\nUnable to connect to API.")
        return None

    except ValueError:
        print("\nInvalid JSON response.")
        return None

    if not isinstance(data, list):
        print("\nInvalid API response format.")
        return None

    if not data:
        print("\nNo matching country found.")
        return None

    country_data = next(
        (
            item for item in data
            if isinstance(item, dict)
            and isinstance(item.get("name"), str)
            and item["name"].strip().lower() == country.strip().lower()
        ),
        None
    )

    if country_data is None:
        print("\nNo exact country match found.")
        return None

    name = country_data.get("name")
    capital = country_data.get("capital")
    population = country_data.get("population")
    region = country_data.get("region")
    currencies = country_data.get("currencies")

    if (
        not isinstance(name, str)
        or not isinstance(capital, str)
        or not isinstance(population, int)
        or isinstance(population, bool)
        or not isinstance(region, str)
        or not isinstance(currencies, list)
    ):
        print("\nInvalid API response data.")
        return None

    currency = "Not available"

    if currencies:
        first_currency = currencies[0]

        if not isinstance(first_currency, dict):
            print("\nInvalid currency information.")
            return None

        code = first_currency.get("code")
        currency_name = first_currency.get("name")

        if isinstance(code, str):
            currency = code

            if isinstance(currency_name, str):
                currency += f" ({currency_name})"

    return {
        "name": name,
        "capital": capital,
        "population": f"{population:,}",
        "region": region,
        "currency": currency
    }


def display_country_info(info):
    if info is None:
        return

    print("\n========== COUNTRY INFORMATION ==========")
    print("Country Name :", info["name"])
    print("Capital      :", info["capital"])
    print("Population   :", info["population"])
    print("Region       :", info["region"])
    print("Currency     :", info["currency"])
    print("==========================================")


def main():
    print("WELCOME TO COUNTRY INFORMATION SYSTEM")

    while True:
        try:
            country = input("\nEnter country name: ")
            country = validate_country_name(country)

            info = fetch_country_data(country)
            display_country_info(info)

        except ValueError as error:
            print("\nInvalid Input:", error)

        choice = input(
            "\nDo you want to search another country? (yes/no): "
        )

        if choice.strip().lower() not in ["yes", "y"]:
            print("\nThank you for using Country Information System!")
            break


if __name__ == "__main__":
    main()
