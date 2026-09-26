#!/usr/bin/env python3

import re
import sys
import webbrowser
from urllib.parse import quote

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier
except ImportError:
    print("[!] Missing dependency: phonenumbers")
    print("[*] Run: pip install phonenumbers")
    sys.exit(1)


BANNER = r"""
╔══════════════════════════════════════════╗
║        🇲🇦 MOROCCO PHONE OSINT          ║
║          Public Information Tool         ║
╚══════════════════════════════════════════╝
"""


def normalize_number(raw):
    number = raw.strip()
    number = number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    if number.startswith("00212"):
        number = "+" + number[2:]

    elif number.startswith("212"):
        number = "+" + number

    elif number.startswith("0"):
        number = "+212" + number[1:]

    return number


def analyze_number(raw):
    number = normalize_number(raw)

    try:
        parsed = phonenumbers.parse(number, "MA")
    except phonenumbers.NumberParseException:
        return None

    if not phonenumbers.is_valid_number(parsed):
        return None

    country = geocoder.description_for_number(parsed, "en")
    operator = carrier.name_for_number(parsed, "en")

    return {
        "international": phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "e164": phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        ),
        "country": country or "Unknown",
        "carrier": operator or "Unknown",
        "type": str(phonenumbers.number_type(parsed)),
    }


def public_search(number):
    encoded = quote(number)

    searches = {
        "Google": f"https://www.google.com/search?q=%22{encoded}%22",
        "Bing": f"https://www.bing.com/search?q=%22{encoded}%22",
        "DuckDuckGo": f"https://duckduckgo.com/?q=%22{encoded}%22",
    }

    print("\n[+] Public search URLs:\n")

    for name, url in searches.items():
        print(f"  {name}: {url}")

    choice = input("\n[?] Open searches in browser? [y/N]: ").lower()

    if choice == "y":
        for url in searches.values():
            webbrowser.open(url)


def main():
    print(BANNER)

    raw = input("[+] Enter Moroccan phone number: ")

    result = analyze_number(raw)

    if not result:
        print("\n[!] Invalid Moroccan phone number.")
        return

    print("\n" + "=" * 45)
    print("             RESULT")
    print("=" * 45)

    print(f"Number       : {result['international']}")
    print(f"E.164        : {result['e164']}")
    print(f"Country/Area : {result['country']}")
    print(f"Carrier      : {result['carrier']}")
    print(f"Type         : {result['type']}")

    print("=" * 45)

    public_search(result["e164"])


if __name__ == "__main__":
    main()
