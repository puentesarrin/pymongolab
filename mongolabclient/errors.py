# -*- coding: utf-8 *-*


class BadAPIKeyFormat(Exception):
    """An exception that will raise when the API key is having a bad format."""

    def __init__(self, api_key):
        message = "API key %r has a bad format." % api_key
        super(BadAPIKeyFormat, self).__init__(message)


class InvalidAPIKey(Exception):
    """An exception that will raise when the API key is invalid."""

    def __init__(self, api_key):
        message = "%r is an invalid API key." % api_key
        super(InvalidAPIKey, self).__init__(message)


class InvalidName(Exception):
    """An exception that will raise when a database name or collection name are
    invalid."""

    def __init__(self, message):
        super(InvalidName, self).__init__(message)


class UnsupportedVersion(Exception):
    """An exception that will raise when the selected version is invalid."""

    def __init__(self, message="Unsupported version"):
        super(UnsupportedVersion, self).__init__(message)


class InvalidUpdateOperator(Exception):
    """An exception that will raise when any update operator is invalid."""

    def __init__(self, operator):
        message = "%r is an invalid update operator." % operator
        super(InvalidUpdateOperator, self).__init__(message)
