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


def make_input_stream(version):
    def make_stream(json_obj):
        stream = io.StringIO()
        json.dump(json_obj, stream)
        stream.seek(0)
        return stream

    def make_input(version):
        return {
            "source": {
                "instance": "staging"
            },
            "version": version
        }

    return make_stream(make_input(version))


class TestCheck(object):

    # @mock.patch("src.history.get_history_txt")
    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_edge_case(self):
        # mock_fn.return_value = mock_history_txt_response()

        version = None

        in_stream = make_input_stream(version)
        result = check.check(in_stream)
        assert result[-5:] == [{'date': '2019-09-19 15:25:16 CDT'},
                               {'date': '2019-09-25 11:30:49 CDT'},
                               {'date': '2019-09-27 10:36:01 CDT'},
                               {'date': '2019-09-30 9:45:49 CDT'},
                               {'date': '2019-10-03 16:12:50 CDT'}]

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_has_newest_release_date(self):
        # mock_fn.return_value = mock_history_txt_response()

        version = {'date': '2019-10-03 16:12:50 CDT'}

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == [version]

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_has_newer_release_dates(self):
        # mock_fn.return_value = mock_history_txt_response()

        version = {'date': '2019-09-27 10:36:01 CDT'}

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == [{'date': '2019-09-27 10:36:01 CDT'},
                          {'date': '2019-09-30 9:45:49 CDT'},
                          {'date': '2019-10-03 16:12:50 CDT'}]

    class TestIn(object):
        @vcr.use_cassette('tests/cassettes/test_in.yaml')
        def test_in(self):
            date = "2019-02-19 10:33:39 CST"
            version = {"version": {"date": date}}
            dest_path = tempfile.mkdtemp()

            in_stream = make_input_stream(version["version"])

            result = in_.in_(dest_path, in_stream)
            assert result == version

            date_data = read_file(os.path.join(dest_path, "version"))
            assert date_data == version["version"]["date"]

            urls_data = read_file(os.path.join(dest_path, "urls.json"))
            assert urls_data == read_file(os.path.join(DATA_DIR, "urls.json"))

            app_version_data = read_file(os.path.join(dest_path, "app_versions.json"))
            assert app_version_data == read_file(os.path.join(DATA_DIR, "app_versions.json"))
