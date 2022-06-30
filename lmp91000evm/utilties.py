import csv

def exportCSV():
    str = "cv"+".csv"
    csv_out = open(str, 'wb')
    mywriter = csv.writer(csv_out)
    for row in zip(t_cv, DATA_cv):
        mywriter.writerow(row)
    csv_out.close()
    w.insert('1.0', "Data exported to .csv succesfully!"+'\n'+'\n')