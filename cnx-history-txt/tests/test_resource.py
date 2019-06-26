import io
import json
import os
from unittest import mock

from src import check

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data")


def read_file(filepath):
    with open(filepath) as infile:
        return infile.read()


def mock_history_txt_response():
    return read_file(os.path.join(DATA_DIR, "history.txt"))


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

    @mock.patch("src.history.get_history_txt")
    def test_edge_case(self, mock_fn):
        mock_fn.return_value = mock_history_txt_response()

        version = None

        in_stream = make_input_stream(version)
        result = check.check(in_stream)
        assert result == [{'date': '2019-01-18 9:05:38 CST'},
                          {'date': '2019-01-23 14:31:36 CST'},
                          {'date': '2019-01-31 8:01:20 CST'},
                          {'date': '2019-02-04 9:55:02 CST'},
                          {'date': '2019-02-18 17:55:06 CST'},
                          {'date': '2019-02-19 10:33:39 CST'},
                          {'date': '2019-02-19 15:29:04 CST'}]

    @mock.patch("src.history.get_history_txt")
    def test_has_newest_release_date(self, mock_fn):
        mock_fn.return_value = mock_history_txt_response()

        version = {"date": "2019-02-19 15:29:04 CST"}

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == [version]

    @mock.patch("src.history.get_history_txt")
    def test_has_newer_release_dates(self, mock_fn):
        mock_fn.return_value = mock_history_txt_response()

        version = {"date": "2019-02-19 10:33:39 CST"}

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == [{"date": "2019-02-19 10:33:39 CST"},
                          {"date": "2019-02-19 15:29:04 CST"}]
