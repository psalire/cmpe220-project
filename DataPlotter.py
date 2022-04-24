import matplotlib.pyplot as plt

class DataPlotter:

    def __init__(self, data, db):
        self.data = data
        self.db = db

    def plotResults(self, title, means, lang, db):
        fig, ax = plt.subplots()
        ax.bar(title, means)

        ax.set_title(f'{lang.capitalize()} Benchmark',
                loc ='center',)
        ax.set_xticklabels(title,rotation=90)

        plt.xlabel('Operation', fontweight ='bold')
        plt.ylabel('Time(ms)', fontweight ='bold')
        plt.savefig(f'{lang}_{db}.png', bbox_inches='tight')
        # plt.show()


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
                self.plotResults(title_op, mean_op, language, self.db)

            title_op.clear()
            mean_op.clear()
