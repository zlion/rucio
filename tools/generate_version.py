# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Martin Barisits, <martin.barisits@cern.ch>, 2017-2019

import os
import subprocess
import sys


def run_git_command(cmd):
    output = subprocess.Popen(["/bin/sh", "-c", cmd], stdout=subprocess.PIPE)
    return output.communicate()[0].strip()


if os.path.isdir('.git'):
    if len(sys.argv) > 1:
        GIT_VERSION = sys.argv[1]
    else:
        GIT_VERSION_CMD = 'git describe --abbrev=4'
        GIT_VERSION = run_git_command(GIT_VERSION_CMD)
    BRANCH_NICK_CMD = 'git branch | grep -Ei "\* (.*)" | cut -f2 -d" "'  # NOQA: W605
    BRANCH_NICK = run_git_command(BRANCH_NICK_CMD)
    REVID_CMD = "git rev-parse HEAD"
    REVID = run_git_command(REVID_CMD)
    REVNO_CMD = "git --no-pager log --oneline | wc -l"
    REVNO = run_git_command(REVNO_CMD)
    VERSION_FILE = open("lib/rucio/vcsversion.py", 'w')
    VERSION_FILE.write("""
'''
This file is automatically generated; Do not edit it. :)
'''
VERSION_INFO = {
    'final': %s,
    'version': '%s',
    'branch_nick': '%s',
    'revision_id': '%s',
    'revno': %s
}
""" % (True, GIT_VERSION, BRANCH_NICK, REVID, REVNO))
    VERSION_FILE.close()

    WEBUI_VERSION_FILE = open("lib/rucio/web/ui/static/webui_version", 'w')
    WEBUI_VERSION_FILE.write('%s' % GIT_VERSION)
    WEBUI_VERSION_FILE.close()
