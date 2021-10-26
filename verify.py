#!/usr/bin/python3
import json
import subprocess
import sys
import unittest
from argparse import ArgumentParser


class TestCase(unittest.TestCase):
    """
    This class is a blank shell that unit tests are dynamically added to
    based on the provided json config file
    """

    def __init__(self, name, config, program, test, test_function, stderr_hide):
        """
        Set local config and add a dynamic test function so the python unittest
        framework will name our test cases nicely
        """
        setattr(TestCase, name, test_function)

        super(TestCase, self).__init__(name)

        self.program = program
        self.test = test
        self.stderr_hide = stderr_hide
        self.config = config

    def run_test_case(self):
        # Can't use pydocs on this one, or the unit test framework finds and prints it on each test
        input_str = self.__parse_test_case_stream(self.test["input"])

        output_str, error_str = self.__run_program_under_test(input_str)

        # Print stderr output for debug utility
        if error_str != "" and not self.stderr_hide:
            print(self.test["name"])
            print(error_str)

        self.__validate_test_output(output_str)

    def __parse_test_case_stream(self, field):
        """
        Parse input as array to make it consistently iterable
        """
        if type(field) is str:
            field = [field]

        result = ""
        for s in field:
            s = s.strip()
            if s:
                result += s + "\n"

        return result

    def __run_program_under_test(self, input_str):
        """
        Launch the test program, give it the test input, collect and return output
        """
        program = subprocess.Popen(
            self.program,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Launch and test program
        try:
            output_str, error_str = program.communicate(input=input_str, timeout=1.0)
        except subprocess.TimeoutExpired:
            program.kill()
            self.fail("Program under test did not complete within the provided timeout")

        return output_str, error_str

    def __validate_test_output(self, output_str):
        """
        Validate the output string of the program meets the verification
        criteria for the test
        """
        if "any_order" not in self.config or self.config["any_order"] != "true":
            self.__validate_exact_output(output_str)
        else:
            self.__validate_any_order_output(output_str)

    def __validate_exact_output(self, output_str):
        """
        Validate that the lines of expected output and the generated output
        contain the same content in the same order
        """
        expected_output = self.__parse_test_case_stream(self.test["output"])

        output_array = output_str.strip().split("\n")
        expected_array = expected_output.strip().split("\n")

        for i in range(max(len(output_array), len(expected_array))):
            self.assertLess(i, len(output_array), "Not enough output lines provided")
            self.assertLess(i, len(expected_array), "Too many output lines provided")
            self.assertEqual(
                output_array[i], expected_array[i], "Incorrect output line"
            )

    def __validate_any_order_output(self, output_str):
        """
        Validate that the lines of expected output and the generated output
        contain the same content in any order
        """
        expected_output = self.__parse_test_case_stream(self.test["output"])

        output_array = output_str.strip().split("\n")
        expected_array = expected_output.strip().split("\n")

        for s in expected_array:
            if s in output_array:
                output_array.remove(s)
            else:
                self.fail(s + " expected but not produced")

        if len(output_array) > 0:
            self.fail(str(output_array) + " extra values produced")


def main():
    args = get_args()
    test_config = parse_test_cases(args.tests)

    # Build up a test suite with the tests listed in the config file
    suite = unittest.TestSuite()
    for test in test_config["tests"]:

        case = TestCase(
            test["name"],
            test_config["config"],
            args.program,
            test,
            TestCase.run_test_case,
            args.stderr_hide,
        )

        suite.addTest(case)

    unittest.TextTestRunner(verbosity=2).run(suite)


def get_args():
    """
    Parse command line options for the verification utility
    """
    parser = ArgumentParser("Codegolf verification utility")

    parser.add_argument(
        "-p",
        "--program",
        help='Command line invocation to start the program under test. "python solution.py", "solution.exe", etc',
        required=True,
    )

    parser.add_argument(
        "-t",
        "--tests",
        help="Path to the json test case definition file",
        required=True,
    )

    parser.set_defaults(stderr_hide=False)
    parser.add_argument(
        "-e",
        "--stderr_hide",
        help="Hide stderr output from program under test",
        action="store_true",
    )

    return parser.parse_args()


def parse_test_cases(test_case_json_file_path):
    """
    Load test cases from a json config file
    """
    with open(test_case_json_file_path) as f:
        test_cases = json.load(f)

    return test_cases


if __name__ == "__main__":
    main()
