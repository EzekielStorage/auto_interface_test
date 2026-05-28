# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
    异常处理
"""


class YamlException(Exception):
    """Custom exception for error reporting."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "\n".join(
            [
                "usecase execution failed",
                "   spec failed: {}".format(self.value),
                "   For more details, see this the document.",
            ]
        )
