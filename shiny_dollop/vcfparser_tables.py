import pandas as pd
import os
import argparse
import sys

# find all heatmap_data2plot_WPG_on_WPG_20210602_vcfparser.txt.xlsx in folder

# need to report AA changes only


def clean_lists(some_list):
    ret_list = []
    if len(some_list) >= 1:
        for i in some_list:
            # print(i[i.index("|")+1:])
            ret_list.append(i[i.index("|")+1:])
        return ret_list
    return ret_list


def format_muts(INPUT):
    df = pd.read_excel(io=INPUT, engine='openpyxl', sheet_name=None)

    # This part prepares the dict for appending the sample lists
    dict_vars = {}
    sample_avgs = {}
    for i in df.keys():

        if i == "UK":
            temp_df = df[i].loc[df[i]["NucName+AAName"] != "A28095T|Orf8:K68Stop"]
            temp_df = temp_df.loc[df[i]["NucName+AAName"] != 'C14676T|Orf1b:P403P']
            df[i] = temp_df
        elif i == "SA":
            temp_df = df[i].loc[df[i]["NucName+AAName"] != 'G22813T|S:K417N']
            df[i] = temp_df

        cur_v = df[i]
        samples = list(cur_v.iloc[:, 13:].columns)
        nuc_list = cur_v.iloc[:, 12:]
        nuc = [[] for g in range(0, len(samples))]
        avgs = [0.0 for h in range(0, len(samples))]
        for ii in samples:
            dict_vars[i] = dict(zip(samples, nuc))
            sample_avgs[i] = dict(zip(samples, avgs))
        for f in nuc_list["NucName+AAName"]:
            temp = nuc_list.loc[nuc_list["NucName+AAName"] == f]
            temp_d = temp.to_dict(orient='list')
            nucs = temp_d["NucName+AAName"][0]
            of_int = list(temp_d.keys())[1:]
            for iii in of_int:
                dict_vars[i][iii].append(nucs)


    # This part is to get the averages:
    var_dict = {}
    for i in df.keys():
        cur_v = df[i] # already dropped uk nucs and SA nucs
        temp = None
        maxes = None
        mins = None
        samples = cur_v.iloc[:, 13:]
        temp = samples.mean(axis=0)
        maxes = samples.max(axis=0)
        mins = samples.min(axis=0)
        var_dict[i] = [temp.to_dict(), maxes.to_dict(), mins.to_dict()]

    big_list = []  # Making one large list to append to the returning dataframe
    for i in dict_vars.keys():
        for ii in dict_vars[i].keys():  # this output is good, maybe ignore teh string though
            else_clean = clean_lists(dict_vars[i][ii])
            big_list.append([ii, i, "  ".join(else_clean), str(len(dict_vars[i][ii])) + " \\ " +
                             str(len(df[i].index)),
                             var_dict[i][0][ii], var_dict[i][1][ii], var_dict[i][2][ii]])
            # print(len(df[i].index), len(dict_vars[i][ii]))
    df_return = pd.DataFrame(big_list, columns=["sample", "VOC", "mutations", "Proportion", "Average", "Max", "Min"])
    return df_return


def crispy_data(start_walk):
    df_crispy = pd.DataFrame(columns=["Bam_file", "Percent_coverage", "avg_depth", "Ns", "missing_positions",
                                      "genome_length"])
    for i in os.walk(start_walk):
        for ii in i[2]:
            if "Crispy_Cody.csv" in ii:
                crispy_paths = str(i[0]) + "\\" + str(ii)
                df1 = pd.read_csv(crispy_paths)
                df_crispy = pd.concat([df_crispy, df1], ignore_index=True)
    return df_crispy.iloc[:, 0:3]


# walk_path = "W:\\Projects\\Project_Chrystal\\2020_SARS-CoV-2_Sewage_Project\\Analyses\\Submitter_Specific_Data" \
#             "\\20210607_Reportables\\"


def check_in_right_dir(some_path):
    counter = 0
    if not os.path.isdir(some_path) or str(some_path) == "":
        print("Invalid path specified")
        sys.exit()
    else:
        for i in os.listdir(some_path):
            if "Reportables" in i:
                counter += 1
        if counter > 2:
            print("Detected too many folders, double check you are in the reportables folder")
            sys.exit()
        else:
            return True


# TODO define path delimiter through macro using os.name (nt for windows, posix for linux)
def main():
    walk_path = ""
    parser = argparse.ArgumentParser(description="Reformat results directories")
    parser.add_argument('-p', '--path', action='store', default=os.getcwd(), help="Path to directory containing results")
    all_samples = pd.DataFrame(columns=["sample", "VOC", "mutations", "Proportion", "Average", "Max", "Min"])
    parsed_args = parser.parse_args()
    print(parsed_args.path)
    if check_in_right_dir(parsed_args.path):
        for i in os.walk(parsed_args.path):
            for ii in i[2]:
                if 'data2plot' in ii and "cov20" not in i[0]:
                    cur_df = None
                    excel_sheet = i[0] + "\\" + str(ii)
                    cur_df = format_muts(excel_sheet)
                    all_samples = all_samples.append(cur_df, ignore_index=True)
        print(all_samples)
        out_path = str(parsed_args.path + "\\" + "Variant_info.csv")
        print(out_path)
        all_samples.to_csv(out_path)
        crispy = crispy_data(parsed_args.path)
        crispy.to_csv(str(parsed_args.path + "\\" + "Coverage_information.csv"))
        ## ready to be written out, Chrystal can combine from here
    else:
        sys.exit("Error: something went wrong :(")


if __name__ == '__main__':
    main()

