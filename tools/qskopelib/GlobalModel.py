"""The GlobalModel module defines a model to display the structure of a file
built from StructBase instances possibly referring to one another."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2008, Python File Format Interface
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

from PyQt4 import QtGui, QtCore

# implementation references:
# http://doc.trolltech.com/4.3/model-view-programming.html
# http://doc.trolltech.com/4.3/model-view-model-subclassing.html
class GlobalModel(QtCore.QAbstractItemModel):
    """General purpose model for QModelIndexed access to data loaded with
    PyFFI."""
    # column definitions
    NUM_COLUMNS = 2
    COL_TYPE = 0
    COL_NAME = 1

    def __init__(self, parent = None, roots = None):
        """Initialize the model to display the given blocks."""
        QtCore.QAbstractItemModel.__init__(self, parent)
        # this list stores the blocks in the view
        # is a list of NiObjects for the nif format, and a list of Chunks for
        # the cgf format
        if roots is None:
            roots = []
        # set up the tree (avoiding duplicate references)
        self.parentDict = {}
        self.refDict = {}
        for root in roots:
            for block in root.tree():
                # create a reference list for this block
                # if it does not exist already
                if not block in self.refDict:
                    self.refDict[block] = []
                for refblock in block.getRefs():
                    # each block can have only one parent
                    if not refblock in self.parentDict:
                        self.parentDict[refblock] = block
                        self.refDict[block].append(refblock)
        # get list of actual roots
        self.roots = []
        # list over all blocks with references
        for root in self.refDict:
            # if it is already listed: skip
            if root in self.roots:
                continue
            # if it has a parent: skip
            if root in self.parentDict:
                continue
            # it must be an actual root
            self.roots.append(root)

    def flags(self, index):
        """Return flags for the given index: all indices are enabled and
        selectable."""
        # all items are enabled and selectable
        if not index.isValid():
            return QtCore.Qt.ItemFlags()
        flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemFlags(flags)

    def data(self, index, role):
        """Return the data of model index in a particular role."""
        # check if the index is valid
        # check if the role is supported
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        # get the data for display
        data = index.internalPointer()

        # the type column
        if index.column() == self.COL_TYPE:
            return QtCore.QVariant(data.__class__.__name__)
        elif index.column() == self.COL_NAME:
            if hasattr(data, "name"):
                return QtCore.QVariant(data.name)
            else:
                return QtCore.QVariant()

        # other colums: invalid
        else:
            return QtCore.QVariant()

    def headerData(self, section, orientation, role):
        """Return header data."""
        if (orientation == QtCore.Qt.Horizontal
            and role == QtCore.Qt.DisplayRole):
            if section == self.COL_TYPE:
                return QtCore.QVariant("Type")
            elif section == self.COL_NAME:
                return QtCore.QVariant("Name")
        return QtCore.QVariant()

    def rowCount(self, parent = QtCore.QModelIndex()):
        """Calculate a row count for the given parent index."""
        if not parent.isValid():
            # top level: one row for each block
            return len(self.roots)
        else:
            # get the parent child count = number of references
            data = parent.internalPointer()
            return len(self.refDict[data])

    def columnCount(self, parent = QtCore.QModelIndex()):
        """Return column count."""
        # column count is constant everywhere
        return self.NUM_COLUMNS

    def index(self, row, column, parent):
        """Create an index to item (row, column) of object parent.
        Internal pointers consist of the BasicBase, StructBase, or Array
        instance."""
        # check if the parent is valid
        if not parent.isValid():
            # parent is not valid, so we need a top-level object
            # return the index with row'th block as internal pointer
            if row < len(self.roots):
                data = self.roots[row]
            else:
                return QtCore.QModelIndex()
        else:
            # parent is valid, so we need to go get the row'th reference
            # get the parent pointer
            data = self.refDict[parent.internalPointer()][row]
        return self.createIndex(row, column, data)

    def parent(self, index):
        """Calculate parent of a given index."""
        # get parent structure
        if not index.isValid():
            return QtCore.QModelIndex()
        data = index.internalPointer()
        # if no parent, then index must be top level object
        if data in self.roots:
            return QtCore.QModelIndex()
        # finally, if parent's parent is not None, then it must be member of
        # some deeper nested structure, so calculate the row as usual
        parentData = self.parentDict[data]
        if parentData in self.roots:
            # top level parent
            # row number is index in roots list
            row = self.roots.index(parentData)
        else:
            # we need the row number of parentData:
            # 1) get the parent of parentData
            # 2) get the list of references of the parent of parentData
            # 3) check the index number of parentData in this list of references
            row = self.refDict[self.parentDict[parentData]].index(parentData)
        # construct the index
        return self.createIndex(row, 0, parentData)
