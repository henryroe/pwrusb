# This file is covered by a different copyright notice from the rest of this project.

# This file provides the astropy_helpers.git_helpers functionality from the astropy_helpers project
# (https://github.com/astropy/astropy-helpers)

# The reason to put this code here, rather than simply `import astropy_helpers.git_helpers` is because
# the astropy_helpers.__init__ module imports matplotlib and sets a matplotlib.use('Agg') which can
# unnecessarily conflict with what the user wants to do.
# e.g.:
# if ztv uses git_helpers from the astropy_helpers project, the following does *not* work as expected 
# in that the plot does not appear after the pylab.show() command.
# (and will work correctly with the fix of calling git_helpers from this file):
#     import ztv
#     import pylab
#     pylab.plot([1,2,3])
#     pylab.show() 

# Copyright notice for this file:
#
# Copyright (c) 2014, Astropy Developers
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of the Astropy Team nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Below this line is unedited version of astropy_helpers/git_helpers.py as of 2016-03-09 12:28MST

# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Utilities for retrieving revision information from a project's git repository.
"""

# Do not remove the following comment; it is used by
# astropy_helpers.version_helpers to determine the beginning of the code in
# this module

# BEGIN

import locale
import os
import subprocess
import warnings


def _decode_stdio(stream):
    try:
        stdio_encoding = locale.getdefaultlocale()[1] or 'utf-8'
    except ValueError:
        stdio_encoding = 'utf-8'

    try:
        text = stream.decode(stdio_encoding)
    except UnicodeDecodeError:
        # Final fallback
        text = stream.decode('latin1')

    return text


def update_git_devstr(version, path=None):
    """
    Updates the git revision string if and only if the path is being imported
    directly from a git working copy.  This ensures that the revision number in
    the version string is accurate.
    """

    try:
        # Quick way to determine if we're in git or not - returns '' if not
        devstr = get_git_devstr(sha=True, show_warning=False, path=path)
    except OSError:
        return version

    if not devstr:
        # Probably not in git so just pass silently
        return version

    if 'dev' in version:  # update to the current git revision
        version_base = version.split('.dev', 1)[0]
        devstr = get_git_devstr(sha=False, show_warning=False, path=path)

        return version_base + '.dev' + devstr
    else:
        #otherwise it's already the true/release version
        return version


def get_git_devstr(sha=False, show_warning=True, path=None):
    """
    Determines the number of revisions in this repository.

    Parameters
    ----------
    sha : bool
        If True, the full SHA1 hash will be returned. Otherwise, the total
        count of commits in the repository will be used as a "revision
        number".

    show_warning : bool
        If True, issue a warning if git returns an error code, otherwise errors
        pass silently.

    path : str or None
        If a string, specifies the directory to look in to find the git
        repository.  If `None`, the current working directory is used, and must
        be the root of the git repository.
        If given a filename it uses the directory containing that file.

    Returns
    -------
    devversion : str
        Either a string with the revision number (if `sha` is False), the
        SHA1 hash of the current commit (if `sha` is True), or an empty string
        if git version info could not be identified.

    """

    if path is None:
        path = os.getcwd()
        if not _get_repo_path(path, levels=0):
            return ''

    if not os.path.isdir(path):
        path = os.path.abspath(os.path.dirname(path))

    if sha:
        # Faster for getting just the hash of HEAD
        cmd = ['rev-parse', 'HEAD']
    else:
        cmd = ['rev-list', '--count', 'HEAD']

    def run_git(cmd):
        try:
            p = subprocess.Popen(['git'] + cmd, cwd=path,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except OSError as e:
            if show_warning:
                warnings.warn('Error running git: ' + str(e))
            return (None, b'', b'')

        if p.returncode == 128:
            if show_warning:
                warnings.warn('No git repository present at {0!r}! Using '
                              'default dev version.'.format(path))
            return (p.returncode, b'', b'')
        if p.returncode == 129:
            if show_warning:
                warnings.warn('Your git looks old (does it support {0}?); '
                              'consider upgrading to v1.7.2 or '
                              'later.'.format(cmd[0]))
            return (p.returncode, stdout, stderr)
        elif p.returncode != 0:
            if show_warning:
                warnings.warn('Git failed while determining revision '
                              'count: {0}'.format(_decode_stdio(stderr)))
            return (p.returncode, stdout, stderr)

        return p.returncode, stdout, stderr

    returncode, stdout, stderr = run_git(cmd)

    if not sha and returncode == 129:
        # git returns 129 if a command option failed to parse; in
        # particular this could happen in git versions older than 1.7.2
        # where the --count option is not supported
        # Also use --abbrev-commit and --abbrev=0 to display the minimum
        # number of characters needed per-commit (rather than the full hash)
        cmd = ['rev-list', '--abbrev-commit', '--abbrev=0', 'HEAD']
        returncode, stdout, stderr = run_git(cmd)
        # Fall back on the old method of getting all revisions and counting
        # the lines
        if returncode == 0:
            return str(stdout.count(b'\n'))
        else:
            return ''
    elif sha:
        return _decode_stdio(stdout)[:40]
    else:
        return _decode_stdio(stdout).strip()


def _get_repo_path(pathname, levels=None):
    """
    Given a file or directory name, determine the root of the git repository
    this path is under.  If given, this won't look any higher than ``levels``
    (that is, if ``levels=0`` then the given path must be the root of the git
    repository and is returned if so.

    Returns `None` if the given path could not be determined to belong to a git
    repo.
    """

    if os.path.isfile(pathname):
        current_dir = os.path.abspath(os.path.dirname(pathname))
    elif os.path.isdir(pathname):
        current_dir = os.path.abspath(pathname)
    else:
        return None

    current_level = 0

    while levels is None or current_level <= levels:
        if os.path.exists(os.path.join(current_dir, '.git')):
            return current_dir

        current_level += 1
        if current_dir == os.path.dirname(current_dir):
            break

        current_dir = os.path.dirname(current_dir)

    return None