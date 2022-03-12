import jpype
import jpype.imports
from jpype.types import *
from importlib import import_module
from os import listdir
import subprocess
import logging
import argparse
import sys

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


def run_benchmark(instance, name):
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
            'category': instance.getCategory(),
            'time': t,
            'success': True,
        }
    except Exception as e:
        logging.error(f'Benchmark "{name}" failed!')
        logging.exception(e)
        return {
            'success': False,
        }


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


def run_java_benchmarks():
    '''
    Load and run java benchmarks from
    package com.cmpe220.benchmark in the jar file
    :return: results
    :rtype: dict
    '''
    java_benchmarks_object = jpype.JPackage('com.cmpe220.benchmark')
    java_benchmarks_list = list(dir(java_benchmarks_object))
    java_benchmarks_list.remove('AbstractBenchmark')
    results = {}
    for bm in java_benchmarks_list:
        logging.info(f'Running benchmark "{bm}"...')
        instance = getattr(java_benchmarks_object, bm)()
        results[bm] = run_benchmark(instance, bm)
    print(results)
    return results


def run_python_benchmarks():
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
        results[module_name] = run_benchmark(instance, module_name)
    print(results)
    return results


def main():
    args = parser.parse_args()

    # Run all Java benchmarks
    if args.no_java is False:
        jpype.startJVM(classpath=[
            f'{JAVA_BENCHMARKS_DIR}/target/{BENCHMARK_JAR_NAME}',
        ])

        compile_success = True
        if args.no_java_compile is False:
            compile_success = compile_java_benchmarks()
        if compile_success:
            run_java_benchmarks()
        else:
            logging.info('Java compiliation failed, skipping benchmarks...')

        jpype.shutdownJVM()

    # Run all Python benchmarks
    if args.no_python is False:
        run_python_benchmarks()


if __name__ == '__main__':
    main()
