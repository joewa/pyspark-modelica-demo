# Copyright (c) 2011, Joerg Raedler (Berlin, Germany)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer. Redistributions in binary form must
# reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import locale
import os


def export(dm, varList, fileName=None, formatOptions={}):
    """Export DyMat data to a CSV file using locale number formatting"""

    if not fileName:
        fileName = dm.fileName+'.l.csv'
    oFile = open(fileName, 'w')

    locale.setlocale(locale.LC_NUMERIC, locale.getdefaultlocale())
    delimiter = formatOptions.get('delimiter', ';')
    newline   = formatOptions.get('newline', os.linesep)

    vDict = dm.sortByBlocks(varList)
    for vList in vDict.values():
        vData = dm.getVarArray(vList)
        vList.insert(0, dm._absc[0])
        oFile.write(delimiter.join(['"%s"'%n for n in vList])+newline)
        for i in range(vData.shape[1]):
            oFile.write(delimiter.join([locale.format('%g', n) for n in vData[:,i]])+newline)

    oFile.close()
