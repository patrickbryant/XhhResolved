from optparse import OptionParser
p = OptionParser()
p.add_option('--output',  type = 'string', default = "", dest = 'outputFile', help = 'output tex name' )
p.add_option('--in',   type = 'string', default = "resolved" , dest = 'inputDir', help = 'input Dir' )
p.add_option('--name', type = 'string', default = "container", dest = 'name', help = 'input Dir' )
p.add_option('-l',     action = 'store_true', default = False , dest = 'doLatex', help = '' )
(o,a) = p.parse_args()

import os, subprocess, shlex

outputDir  = o.outputFile
fileName = outputDir.split("/")[-1]
outputDir = outputDir.replace(fileName,"")


if not os.path.isdir(outputDir):
    os.mkdir(outputDir)


outFile = open(o.outputFile,"w")
baseDir = os.environ['PWD']+"/"

#-------------------------------------------------------------------------------------
def frontMatter(title):
    outFile.write("\documentclass{beamer} \n")
    outFile.write("\mode<presentation>\n")
    outFile.write("\\setbeamertemplate{footline}[frame number]\n")

    outFile.write("{ \usetheme{boxes} }\n")
    outFile.write("\usepackage{times}  % fonts are up to you\n")
    outFile.write("\usefonttheme{serif}  % fonts are up to you\n")
    outFile.write("\usepackage{graphicx}\n")
    outFile.write("\usepackage{colortbl}\n")
    outFile.write("\setlength{\pdfpagewidth}{2\paperwidth}\n")
    outFile.write("\setlength{\pdfpageheight}{2\paperheight}\n")
    outFile.write("\\title{\huge \\textcolor{myblue}{{"+title+"}}}\n")
    outFile.write("\\author{\\textcolor{myred}{{\Large \\\\John Alison\\\\}}\n")
    outFile.write("  \\textit{\Large University of Chicago}\n")
    outFile.write("}\n")
    outFile.write("\\date{  } \n")
    outFile.write("\n")
    outFile.write("\logo{\n")
    outFile.write("\\begin{picture}(10,8)\n")
    outFile.write("\put(8.8,7.3){\includegraphics[width=0.5in]{university_of_chicago_logo.eps}}\n")
    outFile.write("\put(-2.5,7.4){\includegraphics[width=0.55in]{ATLAS-Logo-Square-Blue-RGB.eps}}\n")
    outFile.write("\end{picture}\n")
    outFile.write("}\n")
    outFile.write("\n")
    outFile.write("\unitlength=1cm\n")
    outFile.write("\definecolor{myblue}{RGB}{33,100,158}\n")
    outFile.write("\definecolor{myblack}{RGB}{0,0,0}\n")
    outFile.write("\definecolor{myred}{RGB}{168,56,39}\n")
    outFile.write("\definecolor{UCred}{RGB}{154,52,38}\n")
    outFile.write("\definecolor{mygreen}{RGB}{0,204,0}\n")
    outFile.write("\\begin{document}\n")
    outFile.write("\n")

def makeTextSlide(lines):
    outFile.write("\\begin{frame}\n")
    outFile.write("\\frametitle{\centerline{ \huge \\textcolor{myblack}{Introduction}}}  \n")
    for l in lines:
        outFile.write(l+"\n\n\n")
    outFile.write("\\end{frame}\n")


#-------------------------------------------------------------------------------------
def titleFrame():
    outFile.write("\\begin{frame}\n")
    outFile.write("\\titlepage\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")

    


#-------------------------------------------------------------------------------------
def makeSectionTitle(title):
    outFile.write("\section{"+title+"}\n")
    outFile.write("\\begin{frame}\n")
    outFile.write("  \\begin{flushleft}\n")
    outFile.write("    {\huge \\textcolor{myblack}{"+title+"\\\\ }}\n")
    #outFile.write("    \\textbf{\Huge \\textcolor{myblue}{"+description+"\\\\}}\n")
    outFile.write("    \\vspace{20pt}\n")
    outFile.write("  \\end{flushleft}\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")

#
#
#
def make1by1(title, description, hname):
    outFile.write("\\begin{frame}\n")
    outFile.write("\\frametitle{\centerline{ \huge \\textcolor{myblack}{"+title+"}}}  \n")
    outFile.write("\\begin{picture}(10,8) \n")

    size = 3.0
    x1   =  1.5
    y    = -0.5


    outFile.write("  \put("+str(x1)+","+str(y)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hname+".pdf}}\n")
    outFile.write("  \put(0,6.75){\\textcolor{myred}{\large "+description+"}}\n")


    outFile.write("\\end{picture}\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")



def makeComp(title, description, dir, hName):
    
    make1by2(title, description, [dir+"/iter0/"+hName,
                                  dir+"/iter"+o.iter+"/"+hName])


#
#
#
def make1by2(title, description, hnames):
    outFile.write("\\begin{frame}\n")
    outFile.write("\\frametitle{\centerline{ \huge \\textcolor{myblack}{"+title+"}}}  \n")
    outFile.write("\\begin{picture}(10,8) \n")

    size = 1.8
    x1   = 0.5
    x2   = 5.5
    y1   = 3.4
    y2   = -0.75

    if len(hnames) > 0:
        outFile.write("  \put("+str(x1)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[0]+".pdf}}\n")
    if len(hnames) > 1:
        outFile.write("  \put("+str(x2)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[1]+".pdf}}\n")
    else:
        outFile.write("  \put(-0.5,7.1){\\textcolor{myred}{\large "+description[0]+"}}\n")
        outFile.write("  \put(10,7.1){\\textcolor{myred}{\large "+description[1]+"}}\n")


    outFile.write("\\end{picture}\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")


#
#
#
def make2by2(title, description, hnames):
    outFile.write("\\begin{frame}\n")
    outFile.write("\\frametitle{\centerline{ \huge \\textcolor{myblack}{"+title+"}}}  \n")
    outFile.write("\\begin{picture}(10,8) \n")

    size = 2.0
    
    #
    # Upper Left
    #
    xpos  = 0.5
    ypos  = 3.6
    xdiff = 5.0
    ydiff = -4.15

    x1  = xpos
    y1  = ypos
    x2  = xpos + xdiff
    y2  = ypos + ydiff

    if len(hnames) > 0:
        outFile.write("  \put("+str(x1)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[0]+".pdf}}\n")
    if len(hnames) > 1:
        outFile.write("  \put("+str(x2)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[1]+".pdf}}\n")
    if len(hnames) > 2:
        outFile.write("  \put("+str(x1)+","+str(y2)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[2]+".pdf}}\n")
    if len(hnames) > 3:
        outFile.write("  \put("+str(x2)+","+str(y2)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[3]+".pdf}}\n")
    if len(description) > 2:
        outFile.write("  \put(0,7.1){\\textcolor{myred}{\large "+description[0]+"}}\n")
        outFile.write("  \put(6,7.1){\\textcolor{myred}{\large "+description[1]+"}}\n")
        outFile.write("  \put(0,3.3){\\textcolor{myred}{\large "+description[2]+"}}\n")        
        outFile.write("  \put(6,3.3){\\textcolor{myred}{\large "+description[3]+"}}\n")        
    else:
        outFile.write("  \put(1.,7.75){\\textcolor{myred}{\large "+description[0]+"}}\n")
        outFile.write("  \put(8.5,7.75){\\textcolor{myred}{\large "+description[1]+"}}\n")


    outFile.write("\\end{picture}\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")


#
#
#
def make3Slide(title, description, hnames):
    outFile.write("\\begin{frame}\n")
    outFile.write("\\frametitle{\centerline{ \huge \\textcolor{myblack}{"+title+"}}}  \n")
    outFile.write("\\begin{picture}(10,8) \n")

    size = 1.8
    
    #
    # Upper Left
    #
    xpos  = 0.5
    ypos  = 3.6
    xdiff = 5.0
    ydiff = -4.15

    x1  = xpos
    y1  = ypos
    x2  = xpos + xdiff
    y2  = ypos + ydiff

    if len(hnames) > 0:
        outFile.write("  \put("+str(x1)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[0]+".pdf}}\n")
    if len(hnames) > 1:
        outFile.write("  \put("+str(x2)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+hnames[1]+".pdf}}\n")
    if len(hnames) > 2:
        outFile.write("  \put("+str(x1+xdiff/3)+","+str(y2+0.2)+"){\includegraphics[width="+str(2.4)+"in]{"+baseDir+o.inputDir+"/"+hnames[2]+".pdf}}\n")

    if len(description) > 2:
        outFile.write("  \put(0,7.1){\\textcolor{myred}{\large "+description[0]+"}}\n")
        outFile.write("  \put(6,7.1){\\textcolor{myred}{\large "+description[1]+"}}\n")
        outFile.write("  \put(0,3.3){\\textcolor{myred}{\large "+description[2]+"}}\n")        
        #outFile.write("  \put(6,3.3){\\textcolor{myred}{\large "+description[3]+"}}\n")        
    else:
        outFile.write("  \put(-0.5,7.1){\\textcolor{myred}{\large "+description[0]+"}}\n")
        outFile.write("  \put(10,7.1){\\textcolor{myred}{\large "+description[1]+"}}\n")


    outFile.write("\\end{picture}\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")

#
#
#
def makeTri(title, description, dir, hnames):
    outFile.write("\\begin{frame}\n")
    outFile.write("\\frametitle{\centerline{ \huge \\textcolor{myblack}{"+title+"}}}  \n")
    outFile.write("\\begin{picture}(10,8) \n")

    size = 2.0
    xt   = 2.5
    x1   = -0.1
    x2   = 5.5
    y1   = 3.4
    y2   = -0.5

    outFile.write("  \put("+str(xt)+","+str(y1)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+dir+"/"+hnames[0]+".pdf}}\n")
    outFile.write("  \put("+str(x1)+","+str(y2)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+dir+"/"+hnames[1]+".pdf}}\n")
    outFile.write("  \put("+str(x2)+","+str(y2)+"){\includegraphics[width="+str(size)+"in]{"+baseDir+o.inputDir+"/"+dir+"/"+hnames[2]+".pdf}}\n")
    outFile.write("  \put(2,7.1){\\textcolor{myred}{\large "+description[0]+"}}\n")
    outFile.write("  \put(0,3.3){\\textcolor{myred}{\large "+description[1]+"}}\n")
    outFile.write("  \put(6,3.3){\\textcolor{myred}{\large "+description[2]+"}}\n")

    outFile.write("\\end{picture}\n")
    outFile.write("\\end{frame}\n")
    outFile.write("\n")



    
def drawVars(title,dir1,dir2,vars,labels):

    varList = []
    for v in vars:
        varList.append(dir1+"/"+v)
        varList.append(dir2+"/"+v)

    make2by2(title, labels, 
             varList,
             )

def draw4Vars(title,dirName,vars,labels):

    varList = []
    for v in vars:
        varList.append(dirName+"/"+v)

    make2by2(title, labels, 
             varList,
             )




def PlotVars(title,dirName,labels):

    #
    #  Event Vars
    #
    vars = [
        ["m4j_l",      "m4j_cor_l",  "nJetOther",          "nbJetsOther"],
        ["nPromptElecs_logy",      "nPromptMuons_logy", ],
        ["xhh",        "dhh",        "rhh",                "rRR"],
        ["hCandDphi",  "hCandDr",    "met_trkEt_l_logy",   "mht_l_logy"],
        ["xtt",  "xtt_ave",    "nTopCands_logy",   "nTopCandsAll_logy"],
        ["xtt_2j",  "xtt_2j_ave",    "nTopCands3_logy",   "nTopCandsAll_2j_logy"],
        ]


    for v in vars:
        
        varList = []
        
        for vName in v:
            varList.append(dirName+"/"+vName)

        make2by2(title,
                 labels,
                 varList,
                 )

    #
    #  HCands 
    #
    for hCand in ["leadHCand","sublHCand"]:
        vars = [
            [hCand+"_Eta",   hCand+"_Pt", hCand+"_Mass",  hCand+"_dRjj"],
            ]

        for v in vars:

            varList = []
            
            for vName in v:
                varList.append(dirName+"/"+vName)

            make2by2(title,
                     [hCand,""],
                     varList
                     )        

        for jCand in ["leadJet","sublJet"]:

            jVars = [
                [hCand+"_"+jCand+"_Eta" ,hCand+"_"+jCand+"_Pt", hCand+"_"+jCand+"_Pt_m",hCand+"_"+jCand+"_Pt_s"],
                ]

            for jv in jVars:

                jVarList = []
            
                for jvName in jv:
                    jVarList.append(dirName+"/"+jvName)

                make2by2(title,
                         [hCand+" "+jCand,""],
                         jVarList
                         )        




def PlotComp(title, dirName, postFix, labels):


    #
    #  Event Vars
    #
    vars = [
        ("M4j",("m4j_l","m4j")),
        ("M4j",("m4j_cor_l","m4j_cor")),
        ("M4j",("m4j_cor_l","m4j_diff")),
        ("Other Jets",("nJetOther","otherJets_Pt")),
        ("xhh / dhh ",("dhh","xhh")),
        ("hCand",("hCandDphi","hCandDr")),
        ]

    for v in vars:
        drawVars(v[0], 
                 dirName,
                 v[1],
                 labels=labels
                 )

    #
    #  HCands 
    #
    for hCand in ["leadHCand","sublHCand"]:
        vars = [
            (hCand+" kinematics",(hCand+"_Eta",   hCand+"_Pt")),
            (hCand+" Pt cor",    (hCand+"_Pt_cor",hCand+"_Pt_diff")),
            (hCand+" Mass",      (hCand+"_Mass",  hCand+"_dRjj")),
            ]
        for v in vars:
            drawVars(v[0], dir1, dir2,
                     v[1],
                     labels=labels
                     )        

        for jCand in ["leadJet","sublJet"]:
            jVars = [
                (hCand+" "+jCand, (hCand+"_"+jCand+"_Eta" ,hCand+"_"+jCand+"_Pt"   )),
                (hCand+" "+jCand, (hCand+"_"+jCand+"_Pt_m",hCand+"_"+jCand+"_Pt_s"))
                ]
            for jv in jVars:
                drawVars(jv[0], dir1, dir2,
                         jv[1],
                         labels=labels
                         )        
            

    return

    





#-------------------------------------------------------------------------------------        
def makeTalk():

    #dirName = o.inputDir
    #name    = o.name

    frontMatter("hh4b: \\textcolor{myblack}{Background Modeling} ")

    titleFrame()

    for r in ["Sideband","Control","SignalZZ","SignalHH","HighMet_Sideband","HighMet_Control"]:

        PlotVars(r.replace("_"," "),
                 dirName = r,
                 labels = ["Event Kinematics",""]
                 )

    outFile.write("\\end{document}\n")
    outFile.close()

#-------------------------------------------------------
if __name__ == "__main__":   
    makeTalk()
    
    if o.doLatex: 
        print "Building"
        #cd hist-02-00-02/plots_iter0//PassHCdEta/Data/;pdflatex Nominal_iter0.tex;cd -


        os.chdir(outputDir)
        print outputDir
        os.system("pwd")
        cmd = "pdflatex "+fileName
        #jobs = []
        #
        #jobs.append(subprocess.Popen(shlex.split(cmd)))
        #for job in jobs:
        #    job.wait()
        os.system("pdflatex "+fileName)
        os.chdir(baseDir)
        os.system("pwd")
