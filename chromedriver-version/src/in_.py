import json
import os
import sys


from src.utils import msg, write_file, get_chromedriver_version


def in_(dest_path, in_stream):
    input = json.load(in_stream)
    msg("Input: {}", input)

    version = get_chromedriver_version()
    msg("Version Returned: {}", version)

    # Write out files
    write_file(os.path.join(dest_path, "version"), version)

    return {"version": {"version": version}}


def main():
    dest_path = sys.argv[1]
    msg("Output dir {}", dest_path)
    version = in_(dest_path, sys.stdin)
    print(json.dumps(version))


if __name__ == '__main__':
    main()
