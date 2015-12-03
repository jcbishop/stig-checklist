__author__ = 'jbishop'
import sqlite3
import xlsxwriter
import os, sys
import subprocess


stig_db = sqlite3.connect('stig_checklist.db')

def iterate_scan_res():

    c = stig_db.execute("SELECT stig_id from checklist ORDER BY stig_id")
    chklist_id = c.fetchall()
    num_rows = chklist_id.__len__()
    print num_rows
    currow = 0
    for id in chklist_id:
        currow += 1
        x = id[0]
        try:
            s = stig_db.execute("SELECT description from scan_results where description LIKE '\"" + x + "%'")
        except Exception as e:
            print e
            return -1
        try:
            scan_res = s.fetchall()
        except Exception as e:
            print e
            return -1
        if [[ scan_res is not None ]]:
            num_rows = scan_res.__len__()
            if num_rows >= 2:
                print num_rows
                array_res = []
                for row in scan_res:
                    description = str(row)
                    try:
                        description.index("PASSED")
                        array_res.append("Passed")
                        c.execute( "UPDATE checklist SET compliance=\' \',acceptance=\' \' WHERE stig_id = \'{0}\' AND compliance = ''".format(id[0]))
                        #print description
                    except Exception as e:
                        try:
                            description.index("FAILED")
                            array_res.append("Failed")
                            c.execute( "UPDATE checklist SET compliance=\' \',acceptance=\' \' WHERE stig_id = \'{0}\' AND compliance = ''".format(id[0]))
                            #print description
                            continue
                        except Exception as e:
                            array_res.append("Warning")
                            c.execute( "UPDATE checklist SET compliance=\' \',acceptance=\' \' WHERE stig_id = \'{0}\' AND compliance = ''".format(id[0]))
                            #print description
                            continue
                print array_res
            else:
                results = str(scan_res)
                try:
                    results.index('PASSED')
                    print "%s: PASSED" % id[0]
                    #print results
                    #print ""
                    c.execute( "UPDATE checklist SET compliance=\'Y\',acceptance=\'N\' WHERE stig_id = \'{0}\' AND compliance = ''".format(id[0]))

                except Exception as e:
                    try:
                        results.index('FAILED')
                        print "%s: FAILED" % id[0]
                        #print results
                    #    print ""
                        c.execute( "UPDATE checklist SET compliance=\'N\',acceptance=\'N\' WHERE stig_id = \'{0}\' AND compliance = ''".format(id[0]))

                    except Exception as e:
                        print ""
                        print "{0:s}: Warning".format(id[0])
                        #print results
                        c.execute( "UPDATE checklist SET compliance=\'\',acceptance=\'\' WHERE stig_id = \'{0}\' AND compliance = ''".format(id[0]))

        else:
            continue
    stig_db.commit()
    return


def run_stig_check():
    c = stig_db.execute("SELECT stig_id from checklist ORDER BY stig_id")
    chklist_id = c.fetchall()
    num_rows = chklist_id.__len__()
    print num_rows
    currow = 0
    for stig_id in chklist_id:
        currow += 1
        x = stig_id[0]
	print x
        try:
	    os.chdir("/opt/linux_stigs/rhel6/utils")
	    cmd = "./stig_alt.sh -s {0} -c".format(x)	
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            print(output)
            compliance = output
        except Exception as e:
            print e
            return -1
        try:
            if "PASSED" in compliance:
                cmp = "Y"
            else:
                cmp = "N" 
            print cmp
            stig_db.execute( "UPDATE checklist SET compliance=\'{0}\' WHERE stig_id = \'{1}\'".format(cmp,x))
        except Exception as e:
            print e
            return -1
    stig_db.commit()
    os.chdir("/home/bishojam")
    return



def iterate_checklist():
    f = open('./report.html', 'w')
    c = stig_db.execute("SELECT * from checklist ORDER BY stig_id")
    chklist_id = c.fetchall()
    num_rows = chklist_id.__len__()
    print num_rows
    currow = 0
    f.write("<!DOCTYPE html>")
    f.write('<html lang="en">')
    f.write('<head>')
    f.write('<meta charset="UTF-8">')
    f.write('<title>STIG Report</title>')
    f.write('<style>\
        table {\
            display: table;\
            border-collapse: separate;\
            border-spacing: 2px;\
            border-color: gray;\
        }\
        th {\
            background-color: #4CAF50;\
            color: white;\
        }\
        </style>')
    f.write('</head>')
    f.write("<body>")
    f.write("<table border='1'>")
    f.write("<tr><th>STIG_ID</th><th>COMPLIANCE</th><th>CHECK</th><th>FIX</th></tr>")
    for row in chklist_id:
        line="<tr><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" + row[8] + "</td><td>" + row[9] + "</td></tr>"
        f.write(line)
    f.write("</table>")
    f.write("</body>")
    f.write("</html>")
    return

def write_report():
    c = stig_db.execute("SELECT * from checklist")
    fpath = os.path.curdir
    file = os.path.join(fpath,"stig_results.xlsx")
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    data = c.fetchall()
    if data is None:
        return -1
    else:
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                worksheet.write(i,j,value)
    workbook.close()




def main():
    run_stig_check()

    print "Now generate report..."
    iterate_checklist()

   # iterate_scan_res()

   # write_report()

if __name__ == "__main__":
    main()
