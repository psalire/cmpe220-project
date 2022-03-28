
from BenchmarkFacade import BenchmarkFacade
from importlib import import_module
from os import listdir


class PythonBenchmarkFacade(BenchmarkFacade):

    def run(self):
        '''
        Load and run python benchmarks
        :return: results
        :rtype: dict
        '''
        python_benchmarks_list = listdir(self.args.python_dir)
        python_benchmarks_list.remove('AbstractBenchmark.py')
        python_benchmarks_list = list(filter(
            lambda x: x.endswith('.py'),
            python_benchmarks_list
        ))
        results = {}
        for bm in python_benchmarks_list:
            module_name = bm[:-3]  # rm ".py" from end of filename
            instance = getattr(
                import_module(f'{self.args.python_dir}.{module_name}'),
                module_name,
            )()
            results[module_name] = self.run_benchmark(instance, module_name)
        return results
