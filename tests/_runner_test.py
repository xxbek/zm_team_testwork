from multiprocess.runner import Runner


class TestRunner(Runner):
    __test__ = False

    """Test Runner Class for checking pool and runner work"""
    def __init__(self):
        self._final_data = []

    def start(self, id_link_mapping: tuple) -> tuple:
        """Work in single process"""
        id_cookie, url = id_link_mapping
        process_result = (id_cookie, "Success!", url)

        return process_result

    def end(self, response: tuple) -> None:
        """Work after the end of all processes. Save tested data in runner to check after"""
        self._final_data = response

    def check_pool_work(self):
        """"""
        for elem in self._final_data:
            if len(elem) != 3:
                return False
        return True
