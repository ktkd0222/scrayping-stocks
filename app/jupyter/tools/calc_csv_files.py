import os
import glob
import math
import re
import pandas as pd

files = os.listdir()

# source csv file name
m = re.compile(r'.*(\d+)')
#m = re.compile(r'*_*')
#pd.set_option('display.max_rows', 3000)

out_df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

# concat csv file by stocks
for file in files:
    if not os.path.isfile(file):
        csv_dirs = glob.glob(os.path.join(file, '[0-9][0-9][0-9][0-9]'))

        for csv_dir in csv_dirs:
            df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
            csv_files = glob.glob(os.path.join(csv_dir, '[0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9].csv'))
            # csv_files = glob.glob(os.path.join(os.path.join(file, '4307'), '[0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9].csv'))
            print(f'read csv files -> {csv_files}')
            for csv_file in csv_files:
                #print(f'read file : {csv_file}')
                df_tmp = pd.read_csv(csv_file, header=1, encoding='shift_jis')

                if df_tmp.duplicated(subset='日付').sum() > 0:
                    print(f'Duplicated date data detect. file name:{csv_file}')
                    print(f'auto duplicate recode remove.')
                    df_tmp = df_tmp.drop_duplicates(subset='日付')

                df = df.append(df_tmp, ignore_index=True)
            
            if not len(df) == 0:
                #print(df)
                df = df.sort_values(by=['日付'])
                df = df.reset_index()
                prev_value = 0
                next_value = 0
                prev_values = []
                next_values = []
                print('calc prev and next values start.')
                print(f'source dataframe len -> {len(df)}')
                #print(df)
                # TODO 前日比計算
                for i, row in df.iterrows():
                    if i == 0:
                        # 1行目のみは前日値格納のみ
                        prev_value = row['終値']
                        next_value = row['終値']
                        prev_values.append(0.0)
                        continue

                    #print(f'row - {i} / data - {row["日付"]} / end value - {row["終値"]} / prev_value - {round(row["終値"] - prev_value, 1)} / next_value - {round(row["終値"] - next_value, 1)}')
                    prev_values.append(round(row["終値"] - prev_value, 1))
                    next_values.append(round(row["終値"] - next_value, 1))
                    prev_value = row['終値']
                    next_value = row['終値']
                
                next_values.append(0.0)
                # print()
                label = csv_dir.split('/')[len(csv_dir.split('/')) - 1]
                df[f'{label}_前日比'] = prev_values
                df[f'{label}_翌日比'] = next_values
                #print(df)
                
                output_file = os.path.join(csv_dir, 'output_intermidiate.csv')
                df.to_csv(output_file, index=False)
                if len(out_df) == 0:
                    print('append')
                    out_df = out_df.append(df, ignore_index=True)
                else:
                    print('merge')
                    out_df = pd.merge(out_df, df, on='日付', how='inner')
                print(f'output intermidiate csv file -> {output_file}')
                #print(out_df.columns)

# Column Name check
#print(out_df.columns)
columns = []
for column_name in out_df.columns:
    if column_name == '日付' or m.match(column_name):
        columns.append(column_name)

out_df = out_df[columns]
print(f'Merged file duplicate record num -> {out_df.duplicated(subset="日付").sum()}')

# for dup in out_df.duplicated(subset='日付'):
#     print(dup)
#print()
    
out_df.to_csv('output_calc.csv', index=False)
