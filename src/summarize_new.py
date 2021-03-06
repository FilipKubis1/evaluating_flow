import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import os

np.random.seed(6666)

def summarize(text_file_to_analyze):
    # load of outputs
    data_load = np.loadtxt(text_file_to_analyze)
    data = np.empty_like(data_load)
    # ordering the rows randomly (to simulate the random choice when the weights are identical for different times)
    np.copyto(data, data_load[np.random.rand(len(data)).argsort(kind='mergesort'), :])
    # ordering kills by the weights
    ordering_by_lower_mean_weight = np.min(data[:, [-3, -2]], axis=1)  
    ordered_kills = data[ordering_by_lower_mean_weight.argsort(kind='mergesort'), -1]  # ordering kills by weights
    cummulative_kills = np.cumsum(ordered_kills)
    print(('expected service social cost: ' + str(np.mean(cummulative_kills))))
    print(('service social cost, servicing ratio 100%: ' + str(cummulative_kills[-1])))
    print(('service social cost, servicing ratio 90%: ' + str(cummulative_kills[int(len(cummulative_kills)*0.9)])))
    print(('service social cost, servicing ratio 50%: ' + str(cummulative_kills[int(len(cummulative_kills)*0.5)])))
    print(('expected encounters: ' + str(np.sum(cummulative_kills)/len(cummulative_kills))))

    plt.plot(cummulative_kills)
    plt.savefig(text_file_to_analyze + '.png')
    plt.close()
    # return

    data_plot = np.loadtxt(text_file_to_analyze)
    max_weight = np.max(data_plot[:, -3])
    max_ids = np.max(data_plot[:, 1])
    plt.plot(data_plot[:, -3]/max_weight, color='r')
    plt.plot(data_plot[:, 1]/max_ids, color='g')
    plt.savefig(text_file_to_analyze + '_correlation.png')
    plt.close()


def plot_all(model_results, labels, filename):
    for idx, text_file_to_ananlyze in enumerate(model_results):

        # load of outputs
        data_load = np.loadtxt(text_file_to_ananlyze)
        data = np.empty_like(data_load)

        # ordering the rows randomly (to simulate the random choice when the weights are identical for different times)
        np.copyto(data, data_load[np.random.rand(len(data)).argsort(kind='mergesort'), :])

        # ordering kills by the weights
        ordering_by_lower_mean_weight = np.min(data[:, [-3, -2]], axis=1)
        ordered_kills = data[ordering_by_lower_mean_weight.argsort(kind='mergesort'), -1]  # ordering kills by weights
        cummulative_kills = np.cumsum(ordered_kills)

        # plot
        plt.plot(cummulative_kills, label=labels[idx])

    # redefine x axis from number of scenarios to percentage

    x = np.arange(11) * 60
    xi = np.arange(11) * 10
    plt.xticks(x, xi)

    # some titles, need to be changed
    #plt.rc('text', usetex=True)
    #plt.rc('font', family='serif')
    #plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
    plt.title('Dependence of service disturbance on servicing ratio')
    plt.legend()
    plt.xlabel('Servicing ratio [%]')
    plt.ylabel('Service disturbance [encounters]')
    plt.savefig(filename)
    plt.show()
    plt.close()


"""

    # POKUS SPECIFICKY PRO DATA !!!
    part_len = 20  # this times 40 seconds
    part_data = np.empty_like(data_load)[:part_len, :]
    new_way_cum = np.zeros(part_len)
    #for i in xrange(6):
    cont = True
    i = -1
    while cont == True:
        i += 1
        if (i+1)*part_len > len(data):
            print(i)
            #print((i+1)*part_len)
            #print(len(data))
            part_data = np.zeros_like(data_load)[:part_len, :]
            part_data[(i+1)*part_len - len(data):, :] += data[i*part_len:, :]
            cont = False
        else:
            np.copyto(part_data, data[i*part_len:(i+1)*part_len, :])
        # ordering kills by the weights
        ordering = np.min(part_data[:, [-3, -2]], axis=1)  
        ordered = data[ordering.argsort(kind='mergesort'), -1]  # ordering kills by weights
        new_way_cum += ordered
    cummulative_kills = np.cumsum(new_way_cum)
    print('improved expected service social cost: ' + str(np.mean(cummulative_kills)))
    print('improved service social cost, servicing ratio 100%: ' + str(cummulative_kills[-1]))
    print('improved service social cost, servicing ratio 90%: ' + str(cummulative_kills[int(len(cummulative_kills)*0.9)]))
    print('improved service social cost, servicing ratio 50%: ' + str(cummulative_kills[int(len(cummulative_kills)*0.5)]))

"""
