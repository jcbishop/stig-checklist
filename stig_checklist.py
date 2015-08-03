__author__ = 'jbishop'
import sqlite3
stig_db = sqlite3.connect('stig_checklist.db')


def iterate_scan_res():

    c = stig_db.execute("SELECT stig_id from checklist")
    chklist_id = c.fetchall()
    for id in chklist_id:
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
                for row in scan_res:
                    description = row
                    print description
            else:
                if [[ "[PASSED]" in scan_res ]]:
                    print "%s: PASSED" % id[0]
                elif [[ "[FAILED]" in scan_res ]]:
                    print "%s: FAILED" % id[0]
                else:
                    print "%s: Warning" % id[0]
        else:
            continue
    return

def main():
    iterate_scan_res()

if __name__ == "__main__":
    main()
