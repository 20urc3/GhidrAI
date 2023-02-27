#GhidrAI - An Integrated AI in Ghidra.
#@author 2ourc3 (www.bushido-sec.com)
#@category AI
#@keybinding ctrl shift a
#@menupath Tools.Ghidrai
#@toolbar Ghidrai

import os, xmlrpc, subprocess, re, sys
from time import sleep
from xmlrpc.client import ServerProxy
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor


def get_global():

    """
    Get global informations of the binary
    """

    infos = []
    state = getState()
    project = state.getProject()
    locator = project.getProjectData().getProjectLocator()
    projectMgr = project.getProjectManager()
    activeProject = projectMgr.getActiveProject()
    projectData = activeProject.getProjectData()
    rootFolder = projectData.getRootFolder()
    infos.append(str(state) + str(project) + str(locator) + str(projectMgr) + str(activeProject) + str(projectData))
    return infos


def get_funcs():

    """
    Retrieving functions from the binary
    """

    func = getFirstFunction()
    funcList = []
    nameList = []
    entryList = []
    while func is not None:
        name = ("{}".format(func.getName()))
        entry_point = ("0x{}".format(func.getEntryPoint()))
        func = getFunctionAfter(func)
        nameList.append(str(name))
        entryList.append(str(entry_point))
    names = nameList
    entries = entryList
    return names, entries


def get_namedBlocks():

    """
    Generating block names
    """

    blocks = currentProgram.getMemory().getBlocks()
    nameList = []
    for block in blocks:
        string=("Name: {}, Size: {}".format(block.getName(), block.getSize()))
        nameList.append(string)
    names = str(nameList)
    return names

def get_allXREF():
    
    """
    Generating XREF from the binary
    """

    func = getFirstFunction()
    xref = []
    while func is not None:
        entry_point = func.getEntryPoint()
        reference = getReferencesTo(entry_point)
        func = getFunctionAfter(func)
        xref.append(reference)
    xrefs = xref
    return xrefs


def get_decomp():
    
    """
    Generating pseudo code of the functions
    """

    program = getCurrentProgram()
    ifc = DecompInterface()
    ifc.openProgram(program)
    func = getFirstFunction()
    decompiled = []
    while func is not None:
        function = func
        results = ifc.decompileFunction(function, 0, ConsoleTaskMonitor())
        decompiled.append(str(results.getDecompiledFunction().getC()))
        func = getFunctionAfter(func)
    return decompiled

def cleaning_code(text):

    """
    Cleaning the pseudo-code generated by Ghidra
    """

    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'undefined8', '8bytesData', text)
    text = re.sub(r'local_res', 'reservedStack_VAR', text)
    text = re.sub(r'DAT_', 'globalVar', text)
    text = re.sub(r'local_', 'localVar_', text)
    text = re.sub(r'\n(?=\n)', '', text)
    text = re.sub(r'\s{5,}', ' ', text)
    text = re.sub(r'\t+', '', text)
    return text

def analyzing_binary():

    """
    Decompiles all functions, analyze it, generate
    comment and rename variable, export it in a text file
    """

    decompiled_code = get_decomp()
    print("Anlysing the functions with ChatGPT")
    for text in decompiled_code:
        text = cleaning_code(text)
        proxy.analyse_GPT(str(text))
    print("Done.")

proxy = ServerProxy('http://localhost:13337')
analyzing_binary()
