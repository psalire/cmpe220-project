import jpype
# import jpype.imports
from jpype.types import *
from importlib import import_module
from os import listdir
from abc import ABC, abstractmethod
import subprocess
import logging
import argparse
import sys
import json

JAVA_BENCHMARKS_DIR = 'java_benchmarks'
BENCHMARK_JAR_NAME = 'java_benchmarks-1.0-jar-with-dependencies.jar'
PYTHON_BENCHMARKS_DIR = 'python_benchmarks'

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

parser = argparse.ArgumentParser(
    description='CMPE 220 DBMS Benchmarker Framework',
)
parser.add_argument(
    '--no-java-compile',
    action='store_true',
    default=False,
    help='Skip compiliation of Java benchmarks',
)
parser.add_argument(
    '--no-java',
    action='store_true',
    default=False,
    help='Skip all Java benchmarks',
)
parser.add_argument(
    '--no-python',
    action='store_true',
    default=False,
    help='Skip all Python benchmarks',
)


class BenchmarkFacade(ABC):

    def __init__(self, args):
        pass

    def run_benchmark(self, instance, name):
        '''
        Run a benchmark with an instance
        :return: results
        :rtype: dict
        '''
        logging.info(f'Running benchmark "{name}"...')
        try:
            t = instance.benchmark()
            logging.info(f'Time: {t}ms')
            return {
                'category': str(instance.getCategory()),
                'time': float(t),
                'success': True,
            }
        except Exception as e:
            logging.error(f'Benchmark "{name}" failed!')
            logging.exception(e)
            return {
                'success': False,
            }

    @abstractmethod
    def run(self):
        pass


class JavaBenchmarkFacade(BenchmarkFacade):

    @staticmethod
    def compile_java_benchmarks():
        '''
        Compile the benchmarks with maven
        :return: success of compilation
        '''
        logging.info('Compiling Java benchmarks...')
        try:
            ret = subprocess.run(
                'mvn package',
                cwd=JAVA_BENCHMARKS_DIR,
                shell=True,
                capture_output=True,
            )
            ret.check_returncode()
            logging.debug(str(ret.stdout))
            return True
        except subprocess.CalledProcessError:
            logging.error(str(ret.stderr))
            return False

    def __init__(self, args):
        self.compile_success = True
        if args.no_java_compile is False:
            self.compile_success = self.compile_java_benchmarks()
        jpype.startJVM(classpath=[
            f'{JAVA_BENCHMARKS_DIR}/target/{BENCHMARK_JAR_NAME}',
        ])

    def run(self):
        '''
        Load and run java benchmarks from
        package com.cmpe220.benchmark in the jar file
        :return: results
        :rtype: dict
        '''
        if self.compile_success is False:
            logging.info('Java compiliation failed, skipping benchmarks...')
            return {}
        java_benchmarks_object = jpype.JPackage('com.cmpe220.benchmark')
        java_benchmarks_list = list(dir(java_benchmarks_object))
        java_benchmarks_list.remove('AbstractBenchmark')
        results = {}
        for bm in java_benchmarks_list:
            instance = getattr(java_benchmarks_object, bm)()
            results[bm] = self.run_benchmark(instance, bm)

        # TODO: fix shutdownJVM() hangs
        # try:
        #     logging.info('Shutting down JVM...')
        #     jpype.shutdownJVM()
        # except Exception:
        #     logging.error('Failed to shutdown JVM')

        return results


class PythonBenchmarkFacade(BenchmarkFacade):

    def run(self):
        '''
        Load and run python benchmarks
        :return: results
        :rtype: dict
        '''
        python_benchmarks_list = listdir(PYTHON_BENCHMARKS_DIR)
        python_benchmarks_list.remove('AbstractBenchmark.py')
        python_benchmarks_list = list(filter(
            lambda x: x.endswith('.py'),
            python_benchmarks_list
        ))
        results = {}
        for bm in python_benchmarks_list:
            module_name = bm[:-3]  # rm ".py" from end of filename
            instance = getattr(
                import_module(f'{PYTHON_BENCHMARKS_DIR}.{module_name}'),
                module_name,
            )()
            results[module_name] = self.run_benchmark(instance, module_name)
        return results


def main():
    args = parser.parse_args()
    results = {}
    benchmark_instances = {}
    if args.no_java is False:
        benchmark_instances['java'] = JavaBenchmarkFacade(args)
    if args.no_python is False:
        benchmark_instances['python'] = PythonBenchmarkFacade(args)

    # Run all benchmarks
    for name in benchmark_instances:
        logging.info(f'Running {name} benchmarks...')
        results[name] = benchmark_instances[name].run()

    logging.info(json.dumps(results))


if __name__ == '__main__':
    main()
