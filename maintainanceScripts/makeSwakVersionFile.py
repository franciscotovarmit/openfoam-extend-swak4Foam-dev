#! /usr/bin/env python

import sys
from os import path
import re

from subprocess import Popen,PIPE
try:
    output = Popen(["hgg", "branch"], stdout=PIPE).communicate()[0]
    isPackage = (output.find("debian")==0)
except OSError:
    # there is no mercurial
    isPackage=False

readme=open(path.join(path.dirname(sys.argv[0]),"..","README"))

reldate="no date"
verstring="undefined"
extension=""

verline=re.compile("\*\* (.+) - version number : (.+)")

for l in readme.readlines():
    m=verline.match(l)
    if m:
        if isPackage and m.group(1).find("Next")==0:
            print "Keeping the last real version number",verstring
            continue
        reldate=m.group(1)
        grp=m.group(2).split()
        verstring=grp[0]
        extension=" ".join(grp[1:])

vmajor,vminor,vpatch=verstring.split(".")

versionH=path.join(path.dirname(sys.argv[0]),
                   "..",
                   "Libraries",
                   "swak4FoamParsers",
                   "include",
                   "swakVersion.H")

oldContent=open(versionH).read()

new=["// automatically generated by %s" % path.basename(sys.argv[0])]
new.append('#define SWAK_VERSION_STRING "%s"' % verstring)
new.append("#define SWAK_VERSION_MAJOR %s" % vmajor)
new.append("#define SWAK_VERSION_MINOR %s" % vminor)
new.append("#define SWAK_VERSION_PATCH %s" % vpatch)
new.append('#define SWAK_RELEASE_DATE "%s"' % reldate)
if extension!="":
    new.append('#define SWAK_VERSION_EXTENSION "%s"' % extension)

newContent="\n".join(new)+"\n"

if newContent!=oldContent:
    print "Contents of",versionH,"differ ... writing"
    open(versionH,"w").write(newContent)
