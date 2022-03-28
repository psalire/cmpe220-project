import jpype
# import jpype.imports
from jpype.types import *
from BenchmarkFacade import BenchmarkFacade
import subprocess
import logging

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)


class JavaBenchmarkFacade(BenchmarkFacade):

    def compile_java_benchmarks(self):
        '''
        Compile the benchmarks with maven
        :return: success of compilation
        '''
        logging.info('Compiling Java benchmarks...')
        try:
            ret = subprocess.run(
                'mvn package',
                cwd=self.args.java_dir,
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
        super().__init__(args)
        if args.no_java_compile is False:
            self.compile_success = self.compile_java_benchmarks()
        else:
            self.compile_success = True
        jpype.startJVM(classpath=[
            f'{self.java_benchmarks}/target/'
            'java_benchmarks-1.0-jar-with-dependencies.jar',
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
