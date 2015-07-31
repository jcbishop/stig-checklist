__author__ = 'jbishop'
import xlrd, os, sys
import sqlite3
conn = sqlite3.connect('nessus_results.db')

def import_scan(xlsfile):
    c = conn.cursor()
    # Create table
    try:
        c.execute('''CREATE TABLE scan_results (plugin_id text, cve text, cvss text, risk text, host text, protocol text, port text, name text, synopsis text, description text, solution text, see_also text, plugin_output text)''')
    except Exception as e:
        print e
    fpath = os.path.curdir
    file = os.path.join(fpath,xlsfile)
    workbook = xlrd.open_workbook(file,logfile=sys.stdout)
    worksheets = workbook.sheet_names()
    for worksheetname in worksheets:
        wksht = workbook.sheet_by_name(worksheetname)
        print wksht
        num_rows = wksht.nrows - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            if curr_row < 2:
                continue
            row = str(wksht.row(curr_row))
            num_cols = wksht.ncols
            #Plugin ID	CVE	CVSS	Risk	Host	Protocol	Port	Name	Synopsis	Description	Solution	See Also	Plugin Output
            plugin_id_v = str(wksht.cell_value(curr_row,0))
            cve_v = str(wksht.cell_value(curr_row,1))
            try:
                cvss_v = str(wksht.cell_value(curr_row,2))
            except UnicodeEncodeError as ue:
                print ue
                cvss_v = (wksht.cell_value(curr_row,2))
            risk_v = str(wksht.cell_value(curr_row,3))
            host_v = str(wksht.cell_value(curr_row,4))
            try:
                protocol_v = str(wksht.cell_value(curr_row,5))
            except UnicodeEncodeError as ue:
                print ue
                protocol_v = (wksht.cell_value(curr_row,5))
            port_v = str(wksht.cell_value(curr_row,6))
            name_v = str(wksht.cell_value(curr_row,7))
            try:
                synopsis_v = str(wksht.cell_value(curr_row,8))
            except UnicodeEncodeError as ue:
                print ue
                synopsis_v = (wksht.cell_value(curr_row,8))
            try:
                description_v = str(wksht.cell_value(curr_row,9))
            except UnicodeEncodeError as ue:
                print ue
                description_v = (wksht.cell_value(curr_row,9))
            try:
                solution_v = str(wksht.cell_value(curr_row,10))
            except UnicodeEncodeError as ue:
                print ue
                solution_v = (wksht.cell_value(curr_row,10))
            see_also_v = str(wksht.cell_value(curr_row,11))
            plugin_output_v = str(wksht.cell_value(curr_row,12))

            print "Inserting row %d" % curr_row
            try:
                c.execute('''INSERT INTO scan_results(plugin_id, cve, cvss, risk, host, protocol, port, name, synopsis, description, solution, see_also, plugin_output) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,? )''', (plugin_id_v, cve_v, cvss_v, risk_v, host_v, protocol_v, port_v, name_v, synopsis_v, description_v, solution_v, see_also_v, plugin_output_v))
            except UnicodeEncodeError as ue:
                print ue
                print "failed to insert row"
                print row

    conn.commit()


def main():
    import_scan('RHEL5_172_22_83_165_32-bit_cc3clv_Jul_9_2015.xlsx')

if __name__ == "__main__":
    main()