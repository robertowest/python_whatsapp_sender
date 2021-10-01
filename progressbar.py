""" forma de uso
for i in range(100):
    time.sleep(0.1)
    update_progress("Avance ", i/100.0)
update_progress("Some job", 1)
"""
import time, sys

def lines_in_file(archivo):
    rfp=open(archivo, 'r')
    lineas = len(rfp.readlines())
    rfp.close()
    return lineas


def update_progress(job_title, progress):
    length = 80 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), 
          "{0:.2f}".format(round(progress*100, 2)))
    # msg += " FIN\r\n" if progress >= 1 else "  "
    if progress >= 1: msg += " FIN\r\n" 
    sys.stdout.write(msg)
    sys.stdout.flush()
