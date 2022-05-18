from sys import argv
import pandas as pd 
import argparse


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("filepath", type=str)
    parser.add_argument('-c', '--column', type=str, default='Column A')
    parser.add_argument('-C', '--conc', type=float, default=5)
    parser.add_argument('-V', '--volume', type=float, default=10)

    args = parser.parse_args()
    return args


def calc_dilutions(conc):

    global final_conc
    global final_volume
    # final_conc = 5 #ng/uL
    # final_volume = 10 #uL

    DNA_volume = (final_conc * final_volume) / conc
    water_volume = 10 - DNA_volume

    try:
        assert water_volume > 0
    except:
        raise AssertionError("Water volume cannot be less than 0!")

    return round(DNA_volume, 2), round(water_volume, 2)



if __name__ == '__main__':

    args = parse_arguments()

    fp = args.filepath
    col = args.column
    final_conc = args.conc
    final_volume = args.volume


    qubit = pd.read_excel(fp, index_col=0)
    dilutions = qubit[col].apply(calc_dilutions)
    dilutions = dilutions.apply(pd.Series)
    dilutions.columns = ["DNA (uL)", "Water (uL)"]
    output = pd.concat([qubit, dilutions], axis=1)
    output.to_excel(fp)

    print("Done.")