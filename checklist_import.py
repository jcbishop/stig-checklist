__author__ = 'jbishop'
import xlrd, os, sys
import sqlite3
conn = sqlite3.connect('stig_checklist.db')

def import_stig(xlsfile):
    c = conn.cursor()
    # Create table
    try:
        c.execute('''CREATE TABLE checklist (stig text, severity text, title text, stig_id text, compliance text, comments text, acceptance text, approved text, check_content text, fix text, description text, mac_level text, group_id text, group_title text, rule_id text)''')
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
            if curr_row < 8:
                continue
            row = str(wksht.row(curr_row))
            num_cols = wksht.ncols
            # STIG, Risk Severity, Rule Title, Rule-Version (STIG ID), Compliance status ,Comments,Risk Acceptance Needed?,Risk Acceptance Approved?,Check Content,Fix Text,Description,MAC Level,Group ID,Group Title,Rule ID
            stig_v = str(wksht.cell_value(curr_row,0))
            severity_v = str(wksht.cell_value(curr_row,1))
            try:
                title_v = str(wksht.cell_value(curr_row,2))
            except UnicodeEncodeError as ue:
                print ue
                title_v = (wksht.cell_value(curr_row,2))
            stig_id_v = str(wksht.cell_value(curr_row,3))
            compliance_v = str(wksht.cell_value(curr_row,4))
            try:
                comments_v = str(wksht.cell_value(curr_row,5))
            except UnicodeEncodeError as ue:
                print ue
                comments_v = (wksht.cell_value(curr_row,5))
            acceptance_v = str(wksht.cell_value(curr_row,6))
            approved_v = str(wksht.cell_value(curr_row,7))
            try:
                check_v = str(wksht.cell_value(curr_row,8))
            except UnicodeEncodeError as ue:
                print ue
                check_v = (wksht.cell_value(curr_row,8))
            try:
                fix_v = str(wksht.cell_value(curr_row,9))
            except UnicodeEncodeError as ue:
                print ue
                fix_v = (wksht.cell_value(curr_row,9))
            try:
                description_v = str(wksht.cell_value(curr_row,10))
            except UnicodeEncodeError as ue:
                print ue
                description_v = (wksht.cell_value(curr_row,10))
            mac_level_v = str(wksht.cell_value(curr_row,11))
            group_id_v = str(wksht.cell_value(curr_row,12))
            group_title_v = str(wksht.cell_value(curr_row,13))
            rule_id_v = str(wksht.cell_value(curr_row,14))

            print "Inserting row %d" % curr_row
            try:
                c.execute('''INSERT INTO checklist(stig, severity, title, stig_id, compliance, comments, acceptance, approved, check_content, fix, description, mac_level, group_id, group_title, rule_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )''', (stig_v, severity_v, title_v, stig_id_v, compliance_v, comments_v, acceptance_v, approved_v, check_v, fix_v, description_v, mac_level_v, group_id_v, group_title_v, rule_id_v ))
            except UnicodeEncodeError as ue:
                print ue
                print "failed to insert row"
                print row

    conn.commit()


def main():
    import_stig('RHEL5_STIG_V1R10-32bit.xlsx')

if __name__ == "__main__":
    main()