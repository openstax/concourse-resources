import io
import json
import os
import tempfile

import vcr

from src import check, in_

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data")


def read_file(filepath):
    with open(filepath, "r") as infile:
        return infile.read()


def make_stream(json_obj):
    stream = io.StringIO()
    json.dump(json_obj, stream)
    stream.seek(0)
    return stream


def make_input(version):
    payload = {"version": version}

    return payload


def make_input_stream(version):
    return make_stream(make_input(version))


class TestCheck(object):

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_edge_case_no_version(self):
        version = None

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == {"version": "81.0.4044.69"}

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_has_same_version(self):
        version = {"version": "81.0.4044.69"}

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == []

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_has_different_version(self):
        version = {"version": "80.0.4044.69"}

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == {"version": "81.0.4044.69"}


class TestIn(object):
    @vcr.use_cassette('tests/cassettes/test_in.yaml')
    def test_resource_files_are_written(self):
        version = "81.0.4044.69"
        version = {"version": {"version": version}}
        dest_path = tempfile.mkdtemp()

        in_stream = make_input_stream(version["version"])

        result = in_.in_(dest_path, in_stream)
        assert result == version

        version_data = read_file(os.path.join(dest_path, "version"))
        assert version_data == version["version"]["version"]
