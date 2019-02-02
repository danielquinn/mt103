import re
from datetime import date


class MT103:
    """
    Parses an MT103 standard banking format string into a string-like Python
    object so you can do things like `mt103.basic_header` or `print(mt103)`.

    Usage:

    mt103 = MT103("some-mt-103-string")
    print("basic header: {}, bank op code: {}, complete message: {}".format(
        mt103.basic_header,
        mt103.text.bank_operation_code
        mt103
    ))

    With considerable help from:
    http://www.sepaforcorporates.com/swift-for-corporates/read-swift-message-structure/
    https://www.sepaforcorporates.com/swift-for-corporates/explained-swift-gpi-uetr-unique-end-to-end-transaction-reference/
    """

    MESSAGE_REGEX = re.compile(
        r"^"
        r"({1:(?P<basic_header>[^}]+)})?"
        r"({2:(?P<application_header>I[^}]+)})?"
        r"({3:"
            r"(?P<user_header>"
                r"({113:[A-Z]{4}})?"
                r"({108:[A-Z0-9]{0,16}})?"
                r"({111:[0-9]{3}})?"
                r"({121:[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-4[a-zA-Z0-9]{3}-[89ab][a-zA-Z0-9]{3}-[a-zA-Z0-9]{12}})?"  # NOQA: E501
            r")"
        r"})?"
        r"({4:\s*(?P<text>.+?)\s*-})?"
        r"({5:(?P<trailer>[^}]+)})?"
        r"$",
        re.DOTALL
    )

    def __init__(self, message):

        if message is None:
            message = ""

        self.raw = message.strip()
        self.basic_header = None
        self.application_header = None
        self.user_header = None
        self.text = None
        self.trailer = None

        self._boolean = False

        self._populate_by_parsing()

    def __str__(self):
        return self.raw

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return self._boolean
    __nonzero__ = __bool__  # Python 2

    def _populate_by_parsing(self):

        if not self.raw:
            return

        m = self.MESSAGE_REGEX.match(self.raw)

        self._boolean = bool(m)

        if not m:
            return None

        self.basic_header = m.group("basic_header")
        self.application_header = m.group("application_header")
        self.trailer = m.group("trailer")

        self.user_header = UserHeader(m.group("user_header"))
        self.text = Text(m.group("text") or "")


class UserHeader:
    """
    The user header is sufficiently complicated that we might want to break it
    up a bit too.
    """

    REGEX = re.compile(
        r"^"
        r"({113:(?P<bpc>[A-Z]{4})})?"
        r"({108:(?P<mur>[A-Z0-9]{0,16})})?"
        r"({111:(?P<sti>[0-9]{3})})?"
        r"({121:(?P<uetr>[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-4[a-zA-Z0-9]{3}-[89ab][a-zA-Z0-9]{3}-[a-zA-Z0-9]{12})})?"  # NOQA: E501
        r"$"
    )

    def __init__(self, raw):

        self.raw = raw

        self.bank_priority_code = None
        self.message_user_reference = None
        self.service_type_identifier = None
        self.unique_end_to_end_transaction_reference = None

        self._boolean = False

        self._populate_by_parsing()

    def __str__(self):
        return self.raw

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return self._boolean
    __nonzero__ = __bool__  # Python 2

    @property
    def bpc(self):
        return self.bank_priority_code

    @property
    def mur(self):
        return self.message_user_reference

    @property
    def sti(self):
        return self.service_type_identifier

    @property
    def uetr(self):
        return self.unique_end_to_end_transaction_reference

    def _populate_by_parsing(self):

        if not self.raw:
            return

        m = self.REGEX.match(self.raw)

        self._boolean = bool(m)

        if not m:
            return

        self.bank_priority_code = m.group("bpc")
        self.message_user_reference = m.group("mur")
        self.service_type_identifier = m.group("sti")
        self.unique_end_to_end_transaction_reference = m.group("uetr")


class Text:
    """
    With considerable help from:
    https://en.wikipedia.org/wiki/MT103 and
    https://gist.github.com/dmcruz/9940a6b217ff701b8f3e
    """

    REGEX = re.compile(
        r"^"
        r"(:20:(?P<transaction_reference>[^\s:]+)\s*)?"
        r"(:23B:(?P<bank_operation_code>[^\s:]+)\s*)?"
        r"(:32A:"
            r"(?P<value_date_year>\d\d)"  # NOQA
            r"(?P<value_date_month>\d\d)"
            r"(?P<value_date_day>\d\d)"
            r"(?P<interbank_settled_currency>[A-Z]{3})"
            r"(?P<interbank_settled_amount>[\d,]+)"
        r"\s*)?"
        r"(:33B:"
            r"(?P<original_ordered_currency>[A-Z]{3})"
            r"(?P<original_ordered_amount>[\d,]+)"
        r"\s*)?"
        r"(:50[AFK]:(?P<ordering_customer>.*?)\s*(?=(:\d\d)?))?"
        r"(:52[AD]:(?P<ordering_institution>.*?)\s*(?=(:\d\d)?))?"
        r"(:53[ABD]:(?P<sender_correspondent>[^\s:]*)\s*)?"
        r"(:54[ABD]:(?P<receiver_correspondent>.*?)\s*(?=(:\d\d)?))?"
        r"(:56[ACD]:(?P<intermediary>.*?)\s*(?=(:\d\d)?))?"
        r"(:57[ABCD]:(?P<account_with_institution>.*?)\s*(?=(:\d\d)?))?"
        r"(:59A?:(?P<beneficiary>.*?)\s*(?=(:\d\d)?))?"
        r"(:70:(?P<remittance_information>.*?)\s*(?=(:\d\d)?))?"
        r"(:71A:(?P<details_of_charges>.*?)\s*(?=(:\d\d)?))?"
        r"(:72:(?P<sender_to_receiver_information>.*?)\s*(?=(:\d\d)?))?"
        r"(:77A:(?P<regulatory_reporting>.*?)\s*(?=(:\d\d)?))?"
        r"$",
        re.DOTALL
    )

    def __init__(self, raw):

        self.raw = raw

        self.transaction_reference = None
        self.bank_operation_code = None
        self.interbank_settled_currency = None
        self.interbank_settled_amount = None
        self.original_ordered_currency = None
        self.original_ordered_amount = None
        self.ordering_customer = None
        self.ordering_institution = None
        self.sender_correspondent = None
        self.receiver_correspondent = None
        self.intermediary = None
        self.account_with_institution = None
        self.beneficiary = None
        self.remittance_information = None
        self.details_of_charges = None
        self.sender_to_receiver_information = None
        self.regulatory_reporting = None
        self.date = None

        self._boolean = False

        self._populate_by_parsing()

    def __str__(self):
        return self.raw

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return self._boolean
    __nonzero__ = __bool__  # Python 2

    def _populate_by_parsing(self):

        if not self.raw:
            return

        m = self.REGEX.match(self.raw)

        self._boolean = bool(m)

        if not m:
            return

        for k, v in m.groupdict().items():
            if v is None:
                continue
            if k.startswith("value_date_"):
                continue
            setattr(self, k, v)

        try:
            self.date = date(
                2000 + int(m.group("value_date_year")),
                int(m.group("value_date_month")),
                int(m.group("value_date_day"))
            )
        except (ValueError, TypeError):
            pass  # Defaults to None
