import pandas as pd
import numpy as np
import argparse


def csv_to_energy(csv_path):
        """takes a csv file from cpu_monitor and return the energy consumed"""
        idx = pd.Index([],dtype='int64')
        df = pd.read_csv(csv_path,sep=';')
        #df = df.iloc[1: , :]
        #print("df1:", df)
        df = df.drop(labels=1, axis=0) # to delete repetition of a row
        del df[df.columns[-1]] # to delete last column with null values
        #df.drop(index=2)
        #print("new df:",df)
        sub_df = df.filter(regex=("^PW_*"))
        (max_row, max_col) = sub_df.shape
        #print("sub_df: ", sub_df)
        for i in range(0, max_col):
                #print("printed:",sub_df.iloc[:,3])
                idx = idx.union(sub_df[sub_df.iloc[:,i].astype(float)>8000.0].index)

        #print("df2:", df)

        df.drop(idx, inplace=True)
        print('filter out {} rows'.format(idx.size))
        (max_row, max_col) = df.shape
        print('row: {}, col: {}'.format(max_row,max_col))
        df[df.select_dtypes(include=[np.number]).ge(0).all(1)]
        print('row: {}, col: {}'.format(max_row,max_col))

        power_pkg_table = df.filter(regex=("^PW_PKG[0-9]*"))
        power_dram_table = df.filter(regex=("^PW_DRAM[0-9]*"))

        power_row, power_col = power_pkg_table.shape
        pkg = power_col

        print("df3:", df)
        t  = df['TIME'].to_numpy()
        print("t: ",t.astype(float))
        t_min = np.min(t)
        t_max = np.max(t)
        print("t min: ", t_min,"t max: ", t_max)

        dram_energy = 0.0
        pkg_energy = 0.0
        for i in range(0, power_col):
                #print("power_dram df: ")
                #print(power_dram_table.iloc[:,i].astype(float))
                #print("type: ", type(power_dram_table.iloc[:,i].to_numpy()))
                dram_energy += np.trapz(power_dram_table.iloc[:,i].to_numpy().astype(float),t.astype(float))/1000.0
                pkg_energy += np.trapz(power_pkg_table.iloc[:,i].to_numpy().astype(float),t.astype(float))/1000.0

        return dram_energy,pkg_energy,dram_energy+pkg_energy
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='outputs the energy')
    parser.add_argument('-f', '--file', help='Path to input file', required=True)

    args = parser.parse_args()

    dram_energy,pkg_energy,combined = csv_to_energy(args.file) # 1664565
    print("DRAM energy: ",dram_energy)
    print("PKG energy: ",pkg_energy)
    print("DRAM + PKG energy: ", combined)

