import os
import re

def updateSconstruct():
    os.chmod(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"), 0o755)
    fin = open(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"), 'r')
    fout = open(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct1"), 'w')
    for line in fin:
        line=re.sub(r"point\=[\d]+","point="+os.environ["BuildNum"],line)
        fout.write(line)
    fin.close()
    fout.close()
    os.remove(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"))
    os.rename(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct1"),
    os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"))

def updateVersion():
    os.chmod(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"), 0o755)
    fin = open(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"), 'r')
    fout = open(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION1"), 'w')
    for line in fin:
        line=re.sub(r"ADLMSDK_VERSION_POINT=[\d]+","ADLMSDK_VERSION_POINT="+os.environ["BuildNum"],line)
        fout.write(line)
    fin.close()
    fout.close()
    os.remove(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"))
    os.rename(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION1"),
    os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"))

def main():
    updateSconstruct()
    updateVersion()

main()
