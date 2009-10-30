"""
:mod:`pyffi.formats.egm` --- EGM (.egm)
=======================================

Implementation
--------------

.. autoclass:: EgmFormat
   :show-inheritance:
   :members:

Regression tests
----------------

Read a EGM file
^^^^^^^^^^^^^^^

>>> # check and read egm file
>>> stream = open('tests/egm/test.egm', 'rb')
>>> data = EgmFormat.Data()
>>> data.inspect(stream)
>>> # do some stuff with header?
>>> #data.header....
>>> data.read(stream)
>>> # do some stuff...

Parse all EGM files in a directory tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> for stream, data in EgmFormat.walkData('tests/egm'):
...     print(stream.name)
tests/egm/test.egm

Create an EGM file from scratch and write to file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> data = EgmFormat.Data()
>>> from tempfile import TemporaryFile
>>> stream = TemporaryFile()
>>> data.write(stream)
"""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2009, Python File Format Interface
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the Python File Format Interface
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

import struct
import os
import re

import pyffi.object_models.xml
from pyffi.object_models import Common
from pyffi.object_models.xml.Basic import BasicBase
import pyffi.object_models
from pyffi.utils.graph import EdgeFilter

class EgmFormat(pyffi.object_models.xml.FileFormat):
    """This class implements the EGM format."""
    xmlFileName = 'egm.xml'
    # where to look for egm.xml and in what order:
    # EGMXMLPATH env var, or EgmFormat module directory
    xmlFilePath = [os.getenv('EGMXMLPATH'), os.path.dirname(__file__)]
    # file name regular expression match
    RE_FILENAME = re.compile(r'^.*\.egm$', re.IGNORECASE)
    # used for comparing floats
    _EPSILON = 0.0001

    # basic types
    int = Common.Int
    uint = Common.UInt
    byte = Common.Byte
    ubyte = Common.UByte
    char = Common.Char
    short = Common.Short
    ushort = Common.UShort
    float = Common.Float
    PixelData = Common.UndecodedData

    # implementation of egm-specific basic types

    # XXX nothing here yet...

    # XXX only need this if egm files are versioned...
    @staticmethod
    def versionNumber(version_str):
        """Converts version string into an integer.

        :param version_str: The version string.
        :type version_str: str
        :return: A version integer.

        >>> hex(EgmFormat.versionNumber('X'))
        """
        raise NotImplementedError

    class Data(pyffi.object_models.FileFormat.Data):
        """A class to contain the actual egm data."""
        def __init__(self):
            pass

        def inspectQuick(self, stream):
            """Quickly checks if stream contains EGM data, and gets the
            version, by looking at the first 8 bytes.

            :param stream: The stream to inspect.
            :type stream: file
            """
            pos = stream.tell()
            try:
                # XXX check that file is EGM
            finally:
                stream.seek(pos)

        # overriding pyffi.object_models.FileFormat.Data methods

        def inspect(self, stream):
            """Quickly checks if stream contains EGM data, and reads the
            header.

            :param stream: The stream to inspect.
            :type stream: file
            """
            pos = stream.tell()
            try:
                self.inspectQuick(stream)
                # XXX read header
            finally:
                stream.seek(pos)


        def read(self, stream, verbose=0):
            """Read a egm file.

            :param stream: The stream from which to read.
            :type stream: ``file``
            :param verbose: The level of verbosity.
            :type verbose: ``int``
            """
            self.inspectQuick(stream)
            # XXX read the file

            # check if we are at the end of the file
            if stream.read(1):
                raise ValueError(
                    'end of file not reached: corrupt egm file?')
            
        def write(self, stream, verbose=0):
            """Write a egm file.

            :param stream: The stream to which to write.
            :type stream: ``file``
            :param verbose: The level of verbosity.
            :type verbose: ``int``
            """
            # XXX write the file

        # DetailNode

        def getDetailChildNodes(self, edge_filter=EdgeFilter()):
            return []
            # XXX todo, for instance:
            #return self.header.getDetailChildNodes(edge_filter=edge_filter)

        def getDetailChildNames(self, edge_filter=EdgeFilter()):
            # XXX todo, for instance:
            #return self.header.getDetailChildNames(edge_filter=edge_filter)
