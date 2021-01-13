def convertRtype(instructionDetails, inputInstruction, pc):
    registerDetails=open("/home/orkhan7887/Desktop/project/TermProject/regdetails.txt")
    instructionRtype = {"op":"", "rs":"", "rd":"", "rt":"", "shamt":"", "func":"", }

    try:
        for register in registerDetails:
            register = register.split()
            if inputInstruction[1] == register[0]:
                instructionRtype["rd"]=register[1]
            if inputInstruction[2] == register[0]:
                instructionRtype["rs"]=register[1]
            if inputInstruction[3] == register[0]:
                instructionRtype["rt"]=register[1]
    except Exception as e:
        print("The following error has occured: "+str(e))
        return False


    if inputInstruction[3].isdigit()==False or len(inputInstruction)==5:
        instructionRtype["op"] = instructionDetails[2]
        instructionRtype["shamt"] = 0
        instructionRtype["func"] = instructionDetails[3]
    else:
        instructionRtype["op"] = instructionDetails[2]
        instructionRtype["shamt"]=inputInstruction[3]
        instructionRtype["func"]=instructionDetails[3]
        instructionRtype["rt"]=instructionRtype["rs"]
        instructionRtype["rs"]=0

    try:
        output = str(format(int(instructionRtype["op"]), '06b')) + str(format(int(instructionRtype["rs"]), '05b'))+\
            str(format(int(instructionRtype["rt"]), '05b')) + str(format(int(instructionRtype["rd"]), '05b'))+\
            str(format(int(instructionRtype["shamt"]), '05b')) + str(format(int(instructionRtype["func"]), '06b'))

        hexd = (len(output) + 3) // 4
        x = "%.*x" % (hexd, int('0b' + output, 0))
        writeTofile = str(hex(pc)) + ": 0x" + str(x)+"\n"
        f = open("output.obj", "a")
        print(writeTofile)
        f.writelines(writeTofile)
        f.close()

    except Exception as e:
        print(e)
        return False
        

def convertItype(instructionDetails, inputInstruction, pc, code):
    registerDetails=open("/home/orkhan7887/Desktop/project/TermProject/regdetails.txt")
    instructionItype = {"op":"", "rs":"", "rt":"", "const":""}
    
    if len(inputInstruction) == 4:
        if not inputInstruction[3].isdigit():
            try:
                for code_lbl in code:
                    if inputInstruction[3] == code_lbl:
                        inputInstruction[3] = int((code[code.index(inputInstruction[3]) + 1] - (pc + 4)) / 4)
            except Exception as e:
                print(e)
                return False

    elif len(inputInstruction) == 3:
        swLwParentheses = inputInstruction[2].replace("(", " ").replace(")", " ").split()
        try:
            inputInstruction[2] = swLwParentheses[1]
            inputInstruction.append(swLwParentheses[0])
        except Exception as e:
            print(e)
            return False
    try:
        for register in registerDetails:
            register = register.split()
            if inputInstruction[1] == register[0]:
                instructionItype["rt"]=register[1]
            if inputInstruction[2] == register[0]:
                instructionItype["rs"]=register[1]
        instructionItype["op"] = instructionDetails[2]
        instructionItype["const"] = inputInstruction[3]
    except Exception as e:
        print("The following error has occured: "+str(e))
        return False

    try:
        if not isinstance(instructionItype["const"], str) and instructionItype["const"] < 0:
            const = bin(instructionItype["const"] % (1 << 16))
            instructionItype["const"] = int(const, 2)
        elif int(inputInstruction[3]) < 0:
            t = int(inputInstruction[3])
            const = bin(t % (1 << 16))
            instructionItype["const"] = int(const, 2)
    except ValueError:

        print("Label for branch operation is not found!!!")

        return False

    try:
        output = format(int(instructionItype["op"]), '06b') + format(int(instructionItype["rs"]), '05b')+\
            format(int(instructionItype["rt"]), '05b')+ format(int(instructionItype["const"]), '016b')
    except Exception as e:
        print("The following error has occured: "+str(e))
        return False

    hexd = (len(output) + 3) // 4
    
    x = "%.*x" % (hexd, int('0b' + output, 0))
    writeTofile = str(hex(pc)) + ": 0x" + str(x)+"\n"
    print(writeTofile)
    f = open("output.obj", "a")
    f.writelines(writeTofile)
    f.close()


def convertJtype(instructionDetails, inputInstruction, pc, code):
    registerDetails=open("/home/orkhan7887/Desktop/project/TermProject/regdetails.txt")
    instructionJtype = {"op":"", "rs":"", "rt":"", "const":""}
    
    try:
        if not inputInstruction[1].isdigit():
            for code_lbl in code:
                if inputInstruction[1] == code_lbl:
                    temp = code.index(inputInstruction[1]) + 1
                    bin_pc = (code[temp]) & 67108860


                    
        opj = instructionDetails[2]
        labj = bin_pc
        opj = format(int(opj), '06b')
        labj = format(labj, '026b')

        output = str(opj) + str(labj)

        hd = (len(output) + 3) // 4
        x = "%.*x" % (hd, int('0b' + output, 0))
        print(str(hex(pc)) + ": 0x" + str(x))
        f = open("output.obj", "a")
        f.writelines(str(hex(pc)) + ": 0x" + str(x)+"\n")
        f.close()
    except UnboundLocalError:

        print("The label for jump is not found !!!")

        return (1)
    return


def checkInstruction(inputInstruction, pc4):
    isSimpleInstr = inputInstruction[0].isalpha()

    if not isSimpleInstr:
        instruction = inputInstruction[0].split(":")
        if len(instruction) == 2:
            inputInstruction[0] = instruction[1]
        else:
            inputInstruction.pop(0)
    
    instruction_list=open("/home/orkhan7887/Desktop/project/TermProject/instructionList.txt","r")

    for instruction in instruction_list:
        if instruction.split(',')[0] == inputInstruction[0]:
            instructionDetails = instruction
            if inputInstruction[0] == "move":
                inputInstruction[0]="add"
                inputInstruction.append(inputInstruction[2])
                inputInstruction[2]="$0"
            break
    try:
        instructionDetails
    except Exception as e:
        return False
        print("This instruction type isn't supported\n")
    
    code = []
    pcVal=0x80000FFC
    sourceCode=open("/home/orkhan7887/Desktop/project/TermProject/source.src")
    for instR in sourceCode:
        pcVal = pcVal + 4
        if instR.replace(",", "").split()[0].isalpha() == False:
            code.append(instR.replace(",", "").split()[0].split(":")[0])
            code.append(pcVal)
    if instructionDetails.split(',')[1] == 'R':
        convertRtype(instructionDetails.split(','), inputInstruction, pc4)
    elif instructionDetails.split(',')[1] == 'I':
        convertItype(instructionDetails.split(','), inputInstruction, pc4, code)
    else:
        convertJtype(instructionDetails.split(','), inputInstruction, pc4, code)
    return True

def interactive(pc4):
    pc4 = pc4 + 4
    inputI = input("Enter code (ex: add $t0, $t0, $t2)\n").replace(',','').split()
    if not checkInstruction(inputI, pc4):
        if pc4>0x80000FFC:
            pc4 = pc4 - 4
        else:
            pc4 = 0x80000FFC

def batch(pcVal):
    code = open("/home/orkhan7887/Desktop/project/TermProject/source.src", "r")
    c=0
    miss=[]
    for instruction in code:
        pcVal = pcVal + 4
        if not checkInstruction(instruction.replace(',','').split(), pcVal):
            c+=1
            print("Numnber of errors:"+str(c))
            return False
    return True


def main():
    while(True):
        pc4 =0x80000FFC
        m = input("Please choose: i for interactive, b for batch\n")
        choices = {'i':interactive, 'b': batch}
        result = choices.get(m, 'default')
        return result(pc4)


main()