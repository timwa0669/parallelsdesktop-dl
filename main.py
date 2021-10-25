#!/usr/bin/env python3

import argparse
import errno
import sys
import requests
from urllib.parse import urlsplit

program_name = 'pd-dl'
program_description = 'Parallels Desktop downloader'
program_version = '1.0.0'
chunk_size = 16384


def main(main_version, detail_version):
    url = 'https://download.parallels.com/desktop/v' + main_version + \
          '/' + detail_version + '/ParallelsDesktop-' + detail_version + \
          '.dmg?experience=enter_key'
    download_file(url)


def download_file(url):
    local_filename = urlsplit(url).path.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # If chunk:
                f.write(chunk)
    return local_filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=program_name,
        description=program_description
    )
    parser.add_argument('--dlv', nargs='?', type=str, help='download version')
    parser.add_argument('-v', '--version', action='version', version=program_version)
    args = parser.parse_args()
    if args.dlv is None:
        sys.exit(errno.EINVAL)
    version = args.dlv.split('.')
    if len(version) != 3:
        sys.exit(errno.EINVAL)
    main(version[0], args.dlv)
