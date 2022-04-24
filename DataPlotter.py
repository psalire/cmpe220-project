import matplotlib.pyplot as plt
import logging

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

class DataPlotter:

    def __init__(self, data, db):
        self.data = data
        self.db = db

    def plot_means(self, title, means, lang, db):
        try:
            fig, ax = plt.subplots()
            ax.bar(title, means)

            ax.set_title(f'{lang.capitalize()} Benchmark',
                    loc ='center',)
            ax.set_xticklabels(title,rotation=90)

            plt.xlabel('Operation', fontweight ='bold')
            plt.ylabel('Mean Time(ms)', fontweight ='bold')
            fname = f'{lang}_{db}_MEANS.png'
            plt.savefig(fname, bbox_inches='tight')
            logging.info(f'Created plot {fname}')
            # plt.show()
        except Exception as e:
            logging.error('Create plot PNG failed.')
            logging.exception(e)


    def result_display(self):
        title_op = []
        mean_op = []

        for language in self.data.keys():
            for benchmark in self.data[language]:
                benchmark_data = self.data[language][benchmark]

                if benchmark_data['success'] is False:
                    continue

                title_op.append(benchmark)
                mean_op.append(benchmark_data['time']['mean'])

            if len(title_op) > 0:
                self.plot_means(title_op, mean_op, language, self.db)

            title_op.clear()
            mean_op.clear()
