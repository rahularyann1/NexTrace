import phonenumbers
from phonenumbers.phonenumberutil import number_type


def get_number_type(parsed_number):
    """Return a readable phone-number type."""

    types = {
        phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
        phonenumbers.PhoneNumberType.MOBILE: "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        phonenumbers.PhoneNumberType.PAGER: "Pager",
        phonenumbers.PhoneNumberType.UAN: "UAN",
        phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
        phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
    }

    return types.get(number_type(parsed_number), "Unknown")


def validate_phone_input(phone_input):
    """Check basic phone input before attempting analysis."""

    cleaned = phone_input.strip().replace(" ", "").replace("-", "")

    if not cleaned:
        return False, "KuchuPuchu Number Toh Likho Yaar 😭"

    if not cleaned.startswith("+"):
        return False, "KuchuPuchu Yaar Country Code Toh Likho 😭"

    if not cleaned[1:].isdigit():
        return False, "Phone number mein + ke baad sirf digits hone chahiye."

    if len(cleaned[1:]) < 7:
        return False, "Phone number thoda zyada hi chhota hai 😭"

    if len(cleaned[1:]) > 15:
        return False, "Phone number maximum 15 digits ka ho sakta hai."

    return True, cleaned


def get_analysis_status(parsed_number):
    """Return a simple interpretation of the phone-number validation result."""

    valid = phonenumbers.is_valid_number(parsed_number)
    possible = phonenumbers.is_possible_number(parsed_number)

    if valid and possible:
        return "Valid phone number"

    if possible and not valid:
        return "Possible, but not currently valid"

    return "Invalid phone number"