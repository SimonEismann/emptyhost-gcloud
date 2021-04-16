import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statistics

LOADS = ["10", "20", "30", "40"]
MODELS = ["MARS", "WEKA"]

def getMedianPredictionError(measured, prediction, index):
    errors = []
    for k in measured:
        if prediction[k][index] != "":
            new = float(prediction[k][index])
            old = float(measured[k][index])
            errors.append(abs((new - old) / old) * 100)
    if len(errors) > 0:
        return statistics.median(errors)
    else:
        return 0

def createTableWrapperSim(content): # for comparison of standard sim and measurements
    return f"\\begin{{table}}[h]\n\\centering\n\\begin{{tabular}}{{c|ccc|cc}}\n\\hline\nLoad & \\multicolumn{{3}}{{c|}}{{Measured / Predicted Responsetime [ms]}} & \\multicolumn{{2}}{{c}}{{Measured / Predicted Utilization}}  \\\\\n{{[}}Req/s] & A              & B              & C                         & VM1          & VM2  \\\\\n\\hline\n{content}\\hline\n\\end{{tabular}}\n\\caption{{Comparison of measured results and DML simulation results}}\n\\end{{table}}\n"

def createTableEntrySim(load, a, b, c, vm1, vm2):
    return f"{load} & {a} & {b} & {c} & {vm1} & {vm2} \\\\\n"

def createTableWrapperEval(content):
    return f"\\begin{{table}}[h]\n\\centering\n\\begin{{tabular}}{{l|ccc|cc}}\n\\hline\nStatistical & \\multicolumn{{3}}{{c|}}{{Responsetime {{[ms]}}}} & \\multicolumn{{2}}{{c}}{{Utilization}} \\\\\nModel & A & B & C & VM1 & VM2  \\\\ \\hline\n{content}\\end{{tabular}}\n\\caption{{Empty Host problem in red for all loads.}}\n\\label{{Emptyhostresults}}\n\\end{{table}}"

# Measurements
MEAS_RESULTS = {}

# without MARS
SIM_RESULTS = {
    '10': ["72.3", "15.8", "25.7", "0.15", "0.20"],
    '20': ["80.1", "18.8", "28.3", "0.30", "0.40"],
    '30': ["98.7", "26.0", "35.1", "0.45", "0.60"],
    '40': ["153.7", "49.1", "57.7", "0.60", "0.80"]
}

# MARS A, S1
MODEL_RESULTS_A = {
    'MARS': {
        '10': ["77.0", "", "", "", ""],
        '20': ["84.4", "", "", "", ""],
        '30': ["98.6", "", "", "", ""],
        '40': ["130.6", "", "", "", ""]
    },
    'WEKA': {
        '10': ["76.9", "", "", "", ""],
        '20': ["83.9", "", "", "", ""],
        '30': ["95.7", "", "", "", ""],
        '40': ["109.9", "", "", "", ""]
    }
}

# MARS B, S2
MODEL_RESULTS_B = {
    'MARS': {
        '10': ["76.8", "20.9", "25.2", "0.15", "0.12"],
        '20': ["82.4", "23.5", "26.0", "0.30", "0.25"],
        '30': ["92.2", "27.1", "27.5", "0.45", "0.38"],
        '40': ["109.5", "32.2", "30.3", "0.60", "0.50"]
    },
    'WEKA': {
        '10': ["76.7", "20.8", "25.2", "0.15", "0.13"],
        '20': ["82.3", "23.3", "26.0", "0.30", "0.25"],
        '30': ["91.7", "26.5", "27.6", "0.45", "0.38"],
        '40': ["108.2", "30.6", "30.7", "0.60", "0.50"]
    }
}

# MARS C, S3
MODEL_RESULTS_C = {
    'MARS': {
        '10': ["74.6", "15.1", "28.8", "0.15", "0.08"],
        '20': ["80.0", "15.3", "31.7", "0.30", "0.15"],
        '30': ["90.0", "15.8", "36.6", "0.45", "0.22"],
        '40': ["105.1", "16.5", "41.6", "0.60", "0.30"] #!
    },
    'WEKA': {
        '10': ["74.5", "15.1", "28.7", "0.15", "0.08"],
        '20': ["79.6", "15.4", "31.3", "0.30", "0.15"],
        '30': ["88.3", "15.8", "34.9", "0.45", "0.22"],
        '40': ["102.4", "16.5", "39.1", "0.60", "0.30"]
    }
}

# MARS B + C, S2 + S3
MODEL_RESULTS_BC = {
    'MARS': {
        '10': ["79.9", "20.8", "28.4", "0.15", ""],
        '20': ["86.6", "23.5", "30.1", "0.30", ""],
        '30': ["98.0", "27.1", "33.3", "0.45", ""],
        '40': ["115.6", "32.2", "36.4", "0.60", ""] #!
    },
    'WEKA': {
        '10': ["79.9", "20.8", "28.4", "0.15", ""],
        '20': ["86.4", "23.3", "30.2", "0.30", ""],
        '30': ["97.2", "26.5", "33.0", "0.45", ""],
        '40': ["115.2", "30.6", "37.6", "0.60", ""]
    }
}

# STEP 1: create first table comparing simulation to measurements
sim_string = ""
for load in LOADS:
    rt_a = round(pandas.read_csv(f"logs/const_{load}/A_trainingdata.csv")['Response Time'].mean(), 1)
    rt_b = round(pandas.read_csv(f"logs/const_{load}/B_trainingdata.csv")['Response Time'].mean(), 1)
    rt_c = round(pandas.read_csv(f"logs/const_{load}/C_trainingdata.csv")['Response Time'].mean(), 1)
    loadgen_csv = pandas.read_csv(f"loads/scenario_logs/const_{load}.csv")
    util_vm1 = round(loadgen_csv['Watts(Utilization of 34.123.191.220)'].mean(), 2)
    util_vm2 = round(loadgen_csv['Watts(Utilization of 34.68.141.118)'].mean(), 2)
    sim_string += createTableEntrySim(load, f"{rt_a} / {SIM_RESULTS[load][0]}", f"{rt_b} / {SIM_RESULTS[load][1]}", f"{rt_c} / {SIM_RESULTS[load][2]}", f"{util_vm1} / {SIM_RESULTS[load][3]}", f"{util_vm2} / {SIM_RESULTS[load][4]}")
    MEAS_RESULTS[load] = [rt_a, rt_b, rt_c, util_vm1, util_vm2]

writeto = open("eval_latex.txt", "w")
writeto.write(createTableWrapperSim(sim_string))

# STEP 2: create second table comparing MARS/WEKA results
for model in MODELS:
    eval_string = ""
    SIM_RESULTS_A = MODEL_RESULTS_A[model]
    SIM_RESULTS_B = MODEL_RESULTS_B[model]
    SIM_RESULTS_C = MODEL_RESULTS_C[model]
    SIM_RESULTS_BC = MODEL_RESULTS_BC[model]
    for load in LOADS:
        eval_string += f"Measured & {MEAS_RESULTS[load][0]} & {MEAS_RESULTS[load][1]} & {MEAS_RESULTS[load][2]} & {MEAS_RESULTS[load][3]} & {MEAS_RESULTS[load][4]} \\\\\nNone & {SIM_RESULTS[load][0]} & {SIM_RESULTS[load][1]}  & {SIM_RESULTS[load][2]}  & {SIM_RESULTS[load][3]} & {SIM_RESULTS[load][4]} \\\\\nS1 & {SIM_RESULTS_A[load][0]} & - & - & - & - \\\\\nS2 & {SIM_RESULTS_B[load][0]} & {SIM_RESULTS_B[load][1]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_B[load][2]}}}}} & {SIM_RESULTS_B[load][3]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_B[load][4]}}}}} \\\\\nS3 & {SIM_RESULTS_C[load][0]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_C[load][1]}}}}} & {SIM_RESULTS_C[load][2]} & {SIM_RESULTS_C[load][3]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_C[load][4]}}}}} \\\\\nS2 + S3 & {SIM_RESULTS_BC[load][0]} & {SIM_RESULTS_C[load][1]} & {SIM_RESULTS_C[load][2]} & {SIM_RESULTS_C[load][3]} & - \\\\\\hline\n"
    writeto.write(f"{model}:\n")
    writeto.write(createTableWrapperEval(eval_string))

writeto.close()

# STEP 3: draw the median diagram to deviation_median.pdf
def plot_dev_median(model):
    SIM_TABLES = [SIM_RESULTS, MODEL_RESULTS_A[model], MODEL_RESULTS_B[model], MODEL_RESULTS_C[model], MODEL_RESULTS_BC[model]]

    color_palet = sns.color_palette("Blues_d")

    labels = ['None', 'S1', 'S2', 'S3', 'S2 + S3']
    a_means = [getMedianPredictionError(MEAS_RESULTS, t, 0) for t in SIM_TABLES]
    b_means = [getMedianPredictionError(MEAS_RESULTS, t, 1) for t in SIM_TABLES]
    c_means = [getMedianPredictionError(MEAS_RESULTS, t, 2) for t in SIM_TABLES]
    util_a_means = [getMedianPredictionError(MEAS_RESULTS, t, 3) for t in SIM_TABLES]
    util_bc_means = [getMedianPredictionError(MEAS_RESULTS, t, 4) for t in SIM_TABLES]

    x = np.arange(len(labels))  # the label locations
    width = 0.18  # the width of the bars 0.35

    fig, ax = plt.subplots()
    rects_a = ax.bar(x - 2*width, a_means,  width, label='Responsetime A', color=color_palet[0]) # - width/2
    rects_b = ax.bar(x - width, b_means, width, label='Responsetime B', color=color_palet[1]) # + width/2
    rects_c = ax.bar(x, c_means, width, label='Responsetime C', color=color_palet[2])
    rects_util_a = ax.bar(x + width, util_a_means, width, label='Utilization VM1', color=color_palet[3])
    rects_util_bc = ax.bar(x + 2*width, util_bc_means, width, label='Utilization VM2', color=color_palet[4])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Median prediction error over all loads [%]')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = round(rect.get_height(), 1)
            if height != 0:
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

    autolabel(rects_a)
    autolabel(rects_b)
    autolabel(rects_c)
    autolabel(rects_util_a)
    autolabel(rects_util_bc)

    fig.tight_layout()

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10, 5)

    plt.savefig(f"deviation_median_{model}.pdf")
    plt.clf()

for model in MODELS:
    plot_dev_median(model)
