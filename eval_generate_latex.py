import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statistics

LOADS = ["10", "20", "30", "40", "50", "60"]

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
    '10': ["39.7", "15.3", "14.3", "0.05", "0.14"],
    '20': ["41.9", "16.5", "15.4", "0.10", "0.29"],
    '30': ["46.5", "18.8", "17.6", "0.15", "0.43"],
    '40': ["55.3", "23.2", "21.9", "0.20", "0.58"],
    '50': ["74.5", "32.8", "31.3", "0.25", "0.72"],
    '60': ["139.0", "65.0", "63.5", "0.30", "0.87"]
}

# MARS A, S1
SIM_RESULTS_A = {
    '10': ["37.9", "", "", "", ""],
    '20': ["46.6", "", "", "", ""],
    '30': ["60.4", "", "", "", ""],
    '40': ["86.0", "", "", "", ""],
    '50': ["147.9", "", "", "", ""],
    '60': ["323.1", "", "", "", ""]
}

# MARS B, S2
SIM_RESULTS_B = {
    '10': ["45.3", "21.3", "14.1", "0.05", "0.07"],
    '20': ["49.3", "25.1", "14.1", "0.10", "0.14"],
    '30': ["55.1", "30.7", "14.3", "0.15", "0.21"],
    '40': ["64.4", "39.6", "14.5", "0.20", "0.28"],
    '50': ["80.9", "55.6", "14.9", "0.25", "0.35"],
    '60': ["118.2", "92.2", "15.5", "0.30", "0.42"]
}

# MARS C, S3
SIM_RESULTS_C = {
    '10': ["44.2", "15.1", "19.1", "0.05", "0.08"],
    '20': ["49.1", "15.3", "23.7", "0.10", "0.15"],
    '30': ["57.1", "15.7", "31.2", "0.15", "0.23"],
    '40': ["72.2", "16.3", "45.6", "0.20", "0.30"],
    '50': ["109.3", "17.2", "81.7", "0.25", "0.38"],
    '60': ["195.0", "18.5", "165.9", "0.30", "0.45"]
}

# MARS B + C, S2 + S3
SIM_RESULTS_BC = {
    '10': ["48.2", "21.3", "16.9", "0.05", ""],
    '20': ["54.5", "25.1", "19.3", "0.10", ""],
    '30': ["65.3", "30.8", "24.4", "0.15", ""],
    '40': ["86.1", "39.6", "36.2", "0.20", ""],
    '50': ["137.0", "55.7", "71.0", "0.25", ""],
    '60': ["270.5", "92.1", "167.9", "0.30", ""]
}

SIM_TABLES = [SIM_RESULTS, SIM_RESULTS_A, SIM_RESULTS_B, SIM_RESULTS_C, SIM_RESULTS_BC]

# STEP 1: create first table comparing simulation to measurements
sim_string = ""
for load in LOADS:
    rt_a = round(pandas.read_csv(f"logs/const_{load}/A_trainingdata.csv")['Response Time'].mean(), 1)
    rt_b = round(pandas.read_csv(f"logs/const_{load}/B_trainingdata.csv")['Response Time'].mean(), 1)
    rt_c = round(pandas.read_csv(f"logs/const_{load}/C_trainingdata.csv")['Response Time'].mean(), 1)
    loadgen_csv = pandas.read_csv(f"loads/scenario_logs/const_{load}.csv")
    util_vm1 = round(loadgen_csv['Watts(Utilization of 35.225.83.51)'].mean(), 2)
    util_vm2 = round(loadgen_csv['Watts(Utilization of 35.194.16.248)'].mean(), 2)
    sim_string += createTableEntrySim(load, f"{rt_a} / {SIM_RESULTS[load][0]}", f"{rt_b} / {SIM_RESULTS[load][1]}", f"{rt_c} / {SIM_RESULTS[load][2]}", f"{util_vm1} / {SIM_RESULTS[load][3]}", f"{util_vm2} / {SIM_RESULTS[load][4]}")
    MEAS_RESULTS[load] = [rt_a, rt_b, rt_c, util_vm1, util_vm2]

writeto = open("eval_latex.txt", "w")
writeto.write(createTableWrapperSim(sim_string))

# STEP 2: create second table comparing MARS results
eval_string = ""
for load in LOADS:
    eval_string += f"Measured & {MEAS_RESULTS[load][0]} & {MEAS_RESULTS[load][1]} & {MEAS_RESULTS[load][2]} & {MEAS_RESULTS[load][3]} & {MEAS_RESULTS[load][4]} \\\\\nNone & {SIM_RESULTS[load][0]} & {SIM_RESULTS[load][1]}  & {SIM_RESULTS[load][2]}  & {SIM_RESULTS[load][3]} & {SIM_RESULTS[load][4]} \\\\\nS1 & {SIM_RESULTS_A[load][0]} & - & - & - & - \\\\\nS2 & {SIM_RESULTS_B[load][0]} & {SIM_RESULTS_B[load][1]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_B[load][2]}}}}} & {SIM_RESULTS_B[load][3]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_B[load][4]}}}}} \\\\\nS3 & {SIM_RESULTS_C[load][0]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_C[load][1]}}}}} & {SIM_RESULTS_C[load][2]} & {SIM_RESULTS_C[load][3]} & \\textcolor{{red}}{{\\textbf{{{SIM_RESULTS_C[load][4]}}}}} \\\\\nS2 + S3 & {SIM_RESULTS_BC[load][0]} & {SIM_RESULTS_C[load][1]} & {SIM_RESULTS_C[load][2]} & {SIM_RESULTS_C[load][3]} & - \\\\\\hline\n"
writeto.write(createTableWrapperEval(eval_string))

writeto.close()

# STEP 3: draw the median diagram to deviation_median.pdf
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

plt.savefig("deviation_median.pdf")