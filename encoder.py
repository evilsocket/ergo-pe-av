import lief
import numpy as np
import logging as log

classes_replace = {
    'pe-legit': 0,
    'pe-malicious': 1
}

classes = {
    0: 'safe',
    1: 'malicious'
}

properties = [ 'has_configuration',
               'has_debug',
               'has_exceptions',
               'has_exports',
               'has_imports',
               'has_nx',
               'has_relocations',
               'has_resources',
               'has_rich_header',
               'has_signature',
               'has_tls']

libraries = [ "libssp-0", "kernel32", "user32", "advapi32", "oleaut32", "shell32", "ole32", "gdi32", "comctl32", 
            "version", "msvcrt", "comdlg32", "shlwapi", "wininet", "ws2_32", "winmm", "winspool.drv", "wsock32", 
            "msvbvm60", "rpcrt4", "mpr", "psapi", "iphlpapi", "ntdll", "msimg32", "mscoree", "crypt32", "gdiplus", 
            "userenv", "crtdll", "oledlg", "mfc42", "urlmon", "imm32", "rtl100.bpl", "netapi32", "wintrust", "vcl100.bpl", 
            "vcl50.bpl", "uxtheme", "setupapi", "ntoskrnl.pe", "msi", "msvcp60", "lz32", "winhttp", "hal", "core.bpl", 
            "rbrcl1416.bpl", "dbghelp", "api-ms-win-crt-runtime-l1-1-0", "api-ms-win-crt-heap-l1-1-0",
            "api-ms-win-crt-math-l1-1-0", "api-ms-win-crt-stdio-l1-1-0", "api-ms-win-crt-locale-l1-1-0", 
            "oleacc", "komponentyd17.bpl", "job.bpl", "cam.bpl", "vcruntime140", "secur32", "msvcr100", 
            "cxeditorsrs17.bpl", "rasapi32", "api-ms-win-crt-string-l1-1-0", "wtsapi32", "imagehlp", "msvcp140", 
            "cnc.bpl", "indyprotocols190.bpl", "api-ms-win-crt-convert-l1-1-0", "msvcr120", "vcl60.bpl", "rbrcl210.bpl", 
            "rtl170.bpl", "rbide1416.bpl", "rtl60.bpl", "vcl170.bpl", "wldap32", "shfolder", "cxlibraryrs17.bpl", 
            "msvcirt", "report.bpl", "rtl190.bpl", "msvcr90", "api-ms-win-crt-filesystem-l1-1-0", "cxeditorsrs16.bpl",
            "avifil32", "api-ms-win-crt-time-l1-1-0", "jli", "graphic.bpl", "olepro32", "rtl160.bpl", "spmmachine.bpl", 
            "cabinet", "indycore190.bpl", "sacom210.bpl", "rbrtl1416.bpl", "api-ms-win-crt-utility-l1-1-0", "vcl160.bpl", 
            "api-ms-win-crt-environment-l1-1-0", "zcomponent170.bpl", "msvfw32", "libadm_coreutils6", "rbsha",
            "dxpscorers16.bpl", "msacm32", "vcl70.bpl", "applicationmanagement.bpl", "jobgui.bpl", "indyprotocols170.bpl", 
            "rtl70.bpl", "cxed210.bpl", "msvcr80", "libadm_coretinypy6", "ucrtbased", "vcruntime140d", "msvcp120", "msvcp140d", 
            "dinput8", "gui.bpl", "maincontrols.bpl", "rtl120.bpl", "jcl170.bpl", "frx17.bpl", "fs17.bpl", "vcl190.bpl", "sdl2", 
            "machine.bpl", "mfc42u", "normaliz", "sdl2_gfx", "sdl2_ttf", "sdl2_mixer", "msvcp80", "cxgridrs17.bpl", "cxeditorsvcld7.bpl", 
            "libeay32", "cxlibraryd11.bpl", "vcl120.bpl", "gr32_d6.bpl", "cxlibraryrs16.bpl", "cxgridrs16.bpl", "vcl40.bpl", 
            "opengl32", "qt5core", "qtcore4", "wdfldr.sys", "nesting.bpl", "fltmgr.sys"]

# return a list of names of all the features being extracted
# by this encoding algorithm
def attribute_names():
    global properties, libraries
    return properties + \
           ["entrypoint%d" % i for i in range(0, 64)] + \
           ["byte(%02x)" % b for b in range(0, 256)] + \
           ["import(%s)" % l for l in libraries] + \
           ["vsize_ratio", "code_sections_ratio", "pec_sections_ratio", "sections_avg_entropy", "sections_vsize_avg_ratio"]

# encode a few boolean properties as 1.0 (true) or 0.0 (false)
def encode_properties(pe):
    global properties
    props = np.array([0.0] * len(properties))
    for idx, prop in enumerate(properties):
        props[idx] = 1.0 if getattr(pe, prop) else 0.0
    return props

# encode the first 64 bytes of the entrypoint by normalizing to [0.0,1.0]
def encode_entrypoint(ep):
    # pad
    while len(ep) < 64:
        ep += [0.0]
    return np.array(ep) / 255.0 # normalize
                
# return the normalized histogram of each byte frequency
def encode_histogram(raw):
    histo = np.bincount(np.frombuffer(raw, dtype=np.uint8), minlength=256)
    histo = histo / histo.sum() # normalize
    return histo

# encode the API being imported from specific libraries, for each API
# the relative library counter will be incremented
def encode_libraries(pe):
    global libraries

    imports = {dll.name.lower():[api.name if not api.is_ordinal else api.iat_address \
                           for api in dll.entries] for dll in pe.imports}

    libs = np.array([0.0] * len(libraries))
    for idx, lib in enumerate(libraries):
        calls = 0
        dll   = "%s.dll" % lib
        if lib in imports:
            calls = len(imports[lib])
        elif dll in imports:
            calls = len(imports[dll])
        libs[idx] += calls
    tot = libs.sum()
    return ( libs / tot ) if tot > 0 else libs # normalize

# encode a few simple attributes of the PE sections
def encode_sections(pe):
    sections = [{ \
        'characteristics': ','.join(map(str, s.characteristics_lists)),
        'entropy': s.entropy,
        'name': s.name,
        'size': s.size,
        'vsize': s.virtual_size } for s in pe.sections]

    num_sections = len(sections)
    max_entropy  = max([s['entropy'] for s in sections]) if num_sections else 0.0
    max_size     = max([s['size'] for s in sections]) if num_sections else 0.0 
    min_vsize    = min([s['vsize'] for s in sections]) if num_sections else 0.0
    norm_size    = (max_size / min_vsize) if min_vsize > 0 else 0.0

    return [ \
        # code_sections_ratio
        (len([s for s in sections if 'SECTION_CHARACTERISTICS.CNT_CODE' in s['characteristics']]) / num_sections) if num_sections else 0,
        # pec_sections_ratio
        (len([s for s in sections if 'SECTION_CHARACTERISTICS.MEM_EXECUTE' in s['characteristics']]) / num_sections) if num_sections else 0,
        # sections_avg_entropy
        ((sum([s['entropy'] for s in sections]) / num_sections) / max_entropy) if max_entropy > 0 else 0.0,
        # sections_vsize_avg_ratio
        ((sum([s['size'] / s['vsize'] for s in sections]) / num_sections) / norm_size) if norm_size > 0 else 0.0,
    ]

# encode a PE file into a vector of scalars
def encode_pe(filepath):
    log.debug("encoding %s ...", filepath)

    if hasattr(filepath, 'read'):
        raw = filepath.read()
        
    else:
        with open(filepath, 'rb') as fp:
            raw = fp.read()
    
    sz       = len(raw)
    pe       = lief.PE.parse(list(raw)) 
    ep_bytes = [0] * 64
    try:
        ep_offset = pe.entrypoint - pe.optional_header.imagebase
        ep_bytes  = [int(b) for b in raw[ep_offset:ep_offset+64]]
    except Exception as e:
        log.warning("can't get entrypoint bytes from %s: %s", filepath, e)

    v = np.concatenate([ \
        encode_properties(pe),
        encode_entrypoint(ep_bytes),
        encode_histogram(raw),
        encode_libraries(pe),
        [ min(sz, pe.virtual_size) / max(sz, pe.virtual_size)],
        encode_sections(pe)
    ])

    return v
