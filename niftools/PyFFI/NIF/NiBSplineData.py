"""Custom functions for NiBSplineData.

>>> # a doctest
>>> from PyFFI.NIF import NifFormat
>>> block = NifFormat.NiBSplineData()
>>> block.numShortControlPoints = 50
>>> block.shortControlPoints.updateSize()
>>> for i in xrange(block.numShortControlPoints):
...     block.shortControlPoints[i] = 20 - i
>>> block.getShortData(12, 4, 3)
[(8, 7, 6), (5, 4, 3), (2, 1, 0), (-1, -2, -3)]
>>> offset = block.appendShortData([(1,2),(4,3),(13,14),(8,2),(33,33)])
>>> offset
50
>>> block.getShortData(offset, 5, 2)
[(1, 2), (4, 3), (13, 14), (8, 2), (33, 33)]
"""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2008, NIF File Format Library and Tools.
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
#    * Neither the name of the NIF File Format Library and Tools
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

def getShortData(self, offset, num_elements, element_size):
    """Get data.
    
    @param offset: The offset in the data where to start.
    @param num_elements: Number of elements to get.
    @param element_size: Size of a single element.
    @return: A list of C{num_elements} tuples of size C{element_size}.
    """
    # list to store result
    data = []
    # parse the data
    for element in xrange(num_elements):
        data.append(tuple(
            self.shortControlPoints[offset + element * element_size + index]
            for index in xrange(element_size)))
    return data

def appendShortData(self, data):
    """Append data.

    @param data: A list of elements, where each element is a tuple of
        integers.
    @return: The offset at which the data was appended."""
    # get number of elements
    num_elements = len(data)
    # empty list, do nothing
    if num_elements == 0:
        return
    # get element size
    element_size = len(data[0])
    # store offset at which we append the data
    offset = self.numShortControlPoints
    # update size
    self.numShortControlPoints += num_elements * element_size
    self.shortControlPoints.updateSize()
    # store the data
    for element, datum in enumerate(data):
        for index, value in enumerate(datum):
            self.shortControlPoints[
                offset + element * element_size + index] = value
    # return the offset
    return offset

if __name__=='__main__':
    import doctest
    doctest.testmod()