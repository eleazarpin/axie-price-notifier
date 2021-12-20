
import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('basic.py', 'filter6.py', 'filter7.py')
                                                  
                                                                                
def run_process(process):                                                             
    os.system('py .\src\{}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=3)                                                        
pool.map(run_process, processes)