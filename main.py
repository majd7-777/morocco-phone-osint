#!/usr/bin/env python3

import re
import sys
from datetime import datetime

APP_NAME = "MOROCCO PHONE OSINT"
VERSION = "1.0.0"


# =========================
# Terminal colors
# =========================

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"


# =========================
# UI
# =========================

def banner():
    print(f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════╗
║          MOROCCO PHONE OSINT                 ║
║                 v{VERSION}                    ║
╚══════════════════════════════════════════════╝
{RESET}""")


def separator():
    print(f"{BLUE}" + "─" * 48 + f"{RESET}")


def pause():
    input(f"\n{YELLOW}Press ENTER to continue...{RESET}")


# =========================
# Phone normalization
# =========================

def normalize_phone(phone):
    """
    Convert common Moroccan phone formats into +212XXXXXXXXX.
    Examples:
        0612345678
        06 12 34 56 78
        +212612345678
        00212612345678
    """

    phone = phone.strip()

    # Remove spaces, -, (, )
    phone = re.sub(r"[\s\-\(\)]", "", phone)

    # 00212XXXXXXXXX -> +212XXXXXXXXX
    if phone.startswith("00212"):
        phone = "+" + phone[2:]

    # 0XXXXXXXXX -> +212XXXXXXXXX
    elif phone.startswith("0"):
        phone = "+212" + phone[1:]

    # 212XXXXXXXXX -> +212XXXXXXXXX
    elif phone.startswith("212"):
        phone = "+" + phone

    return phone


# =========================
# Moroccan phone validation
# =========================

def validate_moroccan_phone(phone):
    """
    Basic validation for Moroccan mobile numbers.

    Moroccan mobile numbers commonly start with:
        06
        07

    International:
        +2126...
        +2127...
    """

    normalized = normalize_phone(phone)

    pattern = r"^\+212[67][0-9]{8}$"

    return bool(re.fullmatch(pattern, normalized))


# =========================
# Prefix information
# =========================

def get_prefix_info(phone):
    normalized = normalize_phone(phone)

    if not validate_moroccan_phone(normalized):
        return {
            "prefix": "Unknown",
            "type": "Invalid or unsupported Moroccan number"
        }

    local_number = "0" + normalized[4:]

    prefix = local_number[:2]

    if prefix in ("06", "07"):
        number_type = "Mobile"

    else:
        number_type = "Unknown"

    return {
        "prefix": prefix,
        "type": number_type
    }


# =========================
# Number formatting
# =========================

def format_phone(phone):
    normalized = normalize_phone(phone)

    if not normalized.startswith("+212"):
        return normalized

    digits = normalized[4:]

    if len(digits) != 9:
        return normalized

    return (
        "+212 "
        + digits[0:1]
        + " "
        + digits[1:3]
        + " "
        + digits[3:5]
        + " "
        + digits[5:7]
        + " "
        + digits[7:9]
    )


# =========================
# Phone analysis
# =========================

def analyze_phone(phone):
    normalized = normalize_phone(phone)

    result = {
        "input": phone,
        "normalized": normalized,
        "formatted": format_phone(phone),
        "country": "Morocco",
        "country_code": "+212",
        "valid": validate_moroccan_phone(phone),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    prefix_info = get_prefix_info(phone)

    result.update(prefix_info)

    return result


# =========================
# Display phone information
# =========================

def display_phone_info(result):

    separator()

    print(f"{BOLD}{CYAN}PHONE ANALYSIS{RESET}")
    separator()

    print(f"{GREEN}Input       :{RESET} {result['input']}")
    print(f"{GREEN}Normalized  :{RESET} {result['normalized']}")
    print(f"{GREEN}Formatted   :{RESET} {result['formatted']}")
    print(f"{GREEN}Country     :{RESET} {result['country']}")
    print(f"{GREEN}Country Code:{RESET} {result['country_code']}")
    print(f"{GREEN}Prefix      :{RESET} {result['prefix']}")
    print(f"{GREEN}Type        :{RESET} {result['type']}")

    if result["valid"]:
        print(f"{GREEN}Status      : VALID Moroccan number{RESET}")
    else:
        print(f"{RED}Status      : INVALID / unsupported format{RESET}")

    print(f"{GREEN}Checked     :{RESET} {result['timestamp']}")

    separator()


# =========================
# Phone module
# =========================

def phone_module():

    print(f"\n{CYAN}{BOLD}PHONE INFORMATION{RESET}")

    phone = input(
        f"{YELLOW}Enter Moroccan phone number: {RESET}"
    ).strip()

    if not phone:
        print(f"{RED}No number entered.{RESET}")
        return

    result = analyze_phone(phone)

    display_phone_info(result)


# =========================
# Public username module
# =========================

def username_module():

    print(f"""
{CYAN}{BOLD}PUBLIC USERNAME OSINT{RESET}

This module is reserved for checking publicly
available usernames.

It does NOT attempt to log into accounts,
bypass authentication, or access private data.
""")

    username = input(
        f"{YELLOW}Enter public username: {RESET}"
    ).strip()

    if not username:
        print(f"{RED}No username entered.{RESET}")
        return

    username = username.lstrip("@")

    print()
    print(f"{CYAN}Username:{RESET} @{username}")
    print()

    platforms = [
        "Instagram",
        "Facebook",
        "Reddit",
        "X / Twitter",
        "TikTok",
        "GitHub",
        "Telegram",
        "YouTube"
    ]

    print(f"{YELLOW}Supported platforms:{RESET}")

    for platform in platforms:
        print(f"  • {platform}")

    print()
    print(
        f"{BLUE}The actual availability checks will be added "
        f"in the next module.{RESET}"
    )


# =========================
# Authorized network module
# =========================

def network_module():

    print(f"""
{CYAN}{BOLD}AUTHORIZED NETWORK OSINT{RESET}

Use this only with an IP address or domain that
you own or are authorized to test.

The module will later provide:
  • DNS information
  • IP information
  • Open-port detection
  • Service detection
  • Basic security information
""")

    target = input(
        f"{YELLOW}Enter authorized IP/domain: {RESET}"
    ).strip()

    if not target:
        print(f"{RED}No target entered.{RESET}")
        return

    print()
    print(f"{GREEN}Target:{RESET} {target}")

    print(
        f"{BLUE}\nNetwork scanner module will be connected "
        f"in the next stage.{RESET}"
    )


# =========================
# Full report
# =========================

def full_report():

    print(f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════╗
║                FULL OSINT                   ║
╚══════════════════════════════════════════════╝
{RESET}
""")

    phone = input(
        f"{YELLOW}Enter Moroccan phone number: {RESET}"
    ).strip()

    if not phone:
        print(f"{RED}No number entered.{RESET}")
        return

    result = analyze_phone(phone)

    separator()

    print(f"{BOLD}{CYAN}OSINT REPORT{RESET}")

    separator()

    print(f"Generated: {result['timestamp']}")
    print()

    print(f"{GREEN}[PHONE]{RESET}")

    for key, value in result.items():
        print(f"  {key:<15}: {value}")

    separator()

    print(f"""
{YELLOW}Additional modules:{RESET}

  [ ] Public username correlation
  [ ] Public email exposure checks
  [ ] Authorized domain/IP intelligence
  [ ] DNS information
  [ ] Service enumeration
  [ ] JSON report export

These modules will be connected progressively.
""")

    separator()


# =========================
# Menu
# =========================

def menu():

    while True:

        banner()

        print(f"""
{BOLD}Choose an option:{RESET}

{GREEN}[1]{RESET} Phone information
{GREEN}[2]{RESET} Public username OSINT
{GREEN}[3]{RESET} Authorized IP / domain OSINT
{GREEN}[4]{RESET} Full OSINT report
{GREEN}[0]{RESET} Exit
""")

        choice = input(
            f"{YELLOW}OSINT > {RESET}"
        ).strip()

        if choice == "1":
            phone_module()
            pause()

        elif choice == "2":
            username_module()
            pause()

        elif choice == "3":
            network_module()
            pause()

        elif choice == "4":
            full_report()
            pause()

        elif choice == "0":
            print(
                f"\n{GREEN}Goodbye. Stay ethical. 👋{RESET}\n"
            )
            sys.exit(0)

        else:
            print(
                f"{RED}Invalid option.{RESET}"
            )
            pause()


# =========================
# Main
# =========================

if __name__ == "__main__":
    try:
        menu()

    except KeyboardInterrupt:
        print(
            f"\n\n{YELLOW}Interrupted by user.{RESET}"
        )
        sys.exit(0)

    except Exception as error:
        print(
            f"\n{RED}Unexpected error:{RESET} {error}"
        )
        sys.exit(1)
