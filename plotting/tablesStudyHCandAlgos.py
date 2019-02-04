
from optparse import OptionParser
import makeTables

p = OptionParser()
p.add_option('--sampleComp',   type = 'string', default = "", dest = 'sampleComp', help = 'output tex name for sampleComp table' )
p.add_option('--bkgSR',   type = 'string', default = "", dest = 'bkgSR', help = 'output tex name for SR background table' )
p.add_option('--muTable',   type = 'string', default = "", dest = 'mu_qcd_table', help = 'output tex name for mu_qcd table' )
p.add_option('--cutflow_table',   type = 'string', default = "", dest = 'cutflow_table', help = 'output tex name for cutflow table' )
p.add_option('--data',  type = 'string', default = "", dest = 'data',       help = 'data root file' )
p.add_option('--SMNR',  type = 'string', default = "", dest = 'SMNR',       help = 'SMNR root file' )
p.add_option('--m300',  type = 'string', default = "", dest = 'm300',       help = 'm300 root file' )
p.add_option('--m700',  type = 'string', default = "", dest = 'm700',       help = 'm700 root file' )
p.add_option('--m1100',  type = 'string', default = "", dest = 'm1100',       help = 'm1100 root file' )
p.add_option('--ttbar', type = 'string', default = "", dest = 'ttbar',      help = 'ttbar root file' )
p.add_option('--mu',    type = 'string', default = "", dest = 'mu',       help = 'mu_qcd file' )
(o,a) = p.parse_args()


def w(line):
    outFile.write(line+" \n")

outFile = open(o.sampleComp,"w")
table = makeTables.bkgComposition(o.data,o.ttbar,o.mu,False)
for line in table: w(line)
outFile.close()

outFile = open(o.sampleComp.replace(".tex","_unblinded.tex"),"w")
table = makeTables.bkgComposition(o.data,o.ttbar,o.mu,True)
for line in table: w(line)
outFile.close()

outFile = open(o.bkgSR,"w")
table = makeTables.bkgSR(o.data,o.ttbar,o.mu,"",False)
for line in table: w(line)
outFile.close()

outFile = open(o.bkgSR.replace(".tex","_unblinded.tex"),"w")
table = makeTables.bkgSR(o.data,o.ttbar,o.mu,"",True)
for line in table: w(line)
outFile.close()

outFile = open(o.bkgSR.replace(".tex","_ZZ.tex"),"w")
table = makeTables.bkgSR(o.data,o.ttbar,o.mu,"ZZ",True)
for line in table: w(line)
outFile.close()

outFile = open(o.bkgSR.replace(".tex","_HH.tex"),"w")
table = makeTables.bkgSR(o.data,o.ttbar,o.mu,"HH",True)
for line in table: w(line)
outFile.close()

outFile = open(o.mu_qcd_table,"w")
mu_qcd = makeTables.read_mu_qcd_file(o.mu)
w("$ \\mu_{\\rm{QCD}} = ("+str(mu_qcd["mu_qcd_LooseDhhMin"]*1000)[:4]+" \\pm "+str(mu_qcd["mu_qcd_LooseDhhMin_err"]*1000)[:4]+")\\times 10^{-3}$ (stat.)")
outFile.close()


outFile = open(o.cutflow_table,"w")
table = makeTables.compareDataMC(o.data,o.SMNR,o.m300,o.m700,o.m1100,o.ttbar,False)
for line in table: w(line)
outFile.close()

outFile = open(o.cutflow_table.replace(".tex","_unblinded.tex"),"w")
table = makeTables.compareDataMC(o.data,o.SMNR,o.m300,o.m700,o.m1100,o.ttbar,True)
for line in table: w(line)
outFile.close()
