class Autograder():
    ''' Autograder class '''
    def __init__(self, scripts_path, testcases_path, model_answer_filename, total_points):
        self.scripts_path = scripts_path
        self.testcases_path = testcases_path
        self.model_answer_filename = model_answer_filename
        self.total_points = int(total_points)


    def grade(self):
        self._prepare_scripts(self.scripts_path)
        files = self._get_file_names(self.scripts_path)
        cases = self._get_test_cases(self.testcases_path)
        g = self._check_scripts_outputs(self.scripts_path.replace('/','.'), self.model_answer_filename, files, cases, self.total_points)
        return g


    def save_to_csv(self, csv_filename, grade_dict):
        import csv
        with open(csv_filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['ID', 'points', 'test cases'])
            for g in grade_dict:
                csv_writer.writerow([g, grade_dict[g][0], grade_dict[g][1]])


    def _prepare_scripts(self, path_to_scripts):
        from os import listdir, rename
        file_names = listdir(path_to_scripts)
        for f in file_names:
            if f != 'model_ans.py' or '__init__.py':
                new_name = f[-12:]
                rename(path_to_scripts + '/' + f, path_to_scripts + '/' + new_name)


    def _get_file_names(self, path):
        import os
        try:
            file_names = os.listdir(path)
            ###################################################
            # This should be replaced by a smarter way to exclude
            # the model answer and the __init__.py files plus the
            # __pycache__ folder.
            file_names.remove('model_ans.py')
            file_names.remove('__init__.py')
            # file_names.remove('__pycache__')
            file_names = [x[-12:-3] for x in file_names  if (not os.path.isdir(x))]
            ####################################################
        except FileNotFoundError:
            raise FileNotFoundError("The path to quiz answers is not correct.")
        except IndexError:
            raise IndexError("A file name may be incorrect.")
        return file_names


    def _get_test_cases(self, testcases_file):
        try:
            with open(testcases_file, 'r') as f:
                testcases = [x.rstrip() for x in f.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError("test cases file is not found.")
        return testcases


    def _get_args(self, args, type):
        return map(type, args.split())


    def _get_output(self, script_file, testcases):
        from importlib import import_module
        output = []
        try:
            module = import_module(script_file)
            for i, case in enumerate(testcases):
                args = self._get_args(case, int)
                try:
                    output.append(module.gcdIter(*args))
                except:
                    output.append("error in running test case #%d." % i)
        except ModuleNotFoundError:
            output.append('error in importing module "%s".' % script_file)
        except Exception as e:
            output.append(e.args)
        return output


    def _check_scripts_outputs(self, path, model_answer_file, script_files, testcases, total_points):
        points_per_case = total_points / len(testcases)
        grades = {}
        model_answer_output = self._get_output(path + "." + model_answer_file, testcases)
        for f in script_files:
            script_output = self._get_output(path + "." + f, testcases)
            testcases_status = []
            grades[f] = [0, testcases_status, script_output]
            for i, case_output in enumerate(script_output):
                if case_output == model_answer_output[i]:
                    grades[f][0] += points_per_case
                    testcases_status.append(True)
                else:
                    testcases_status.append(False)
        return grades


if __name__ == '__main__':
    params = []
    with open("config.txt", 'r') as conf:
        for line in conf:
            params.append(line.rstrip())

    autograder = Autograder(*params)
    grades = autograder.grade()
    autograder.save_to_csv('grades.csv', grades)

    ########################################################################
    ############################## debug code ##############################
    # for i in grades:
    #     print(i, ":\t grade=", grades[i][0],"\ttest cases=", grades[i][1])
    # from importlib import import_module
    # m = import_module('quiz3.model_ans')
    # print(dir(m))
    ########################################################################