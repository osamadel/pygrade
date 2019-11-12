# PyGrade
PyGrade is an autograder for Python files.

The current version is very limited to the following features:

1. Can run a configurable number of test cases on a configurable number of Python files.
2. Each Python file contains only one function, currently it is called `gcdIter` and it takes two parameters only (however, the code currently accepts a dynamic number of parameters). The function name is not configurable yet.
3. The Autograder can generate a CSV file with the result of the test cases. Some test cases result in an error, in these cases, the test case status output is a list with a single element "error".