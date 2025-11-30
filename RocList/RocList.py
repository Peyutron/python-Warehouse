# Programa para leer la información del archivo plan.xml de Rocrail
# Podemos comprobar los diferentes elementos del plan y sus atributos
#

from tkinter import *
from tkinter import filedialog
import xml.dom.minidom

# Instalar tkinter en Debian:
# sudo apt install python3-tk

# Ruta del archivo Rocrail en Debian
yourfile = '/home/your_user/Rocrail/plan.xml'

# parse the XML file
# Tipos de archivos que abre filedialog XML y todas las extensiones
docs = "null"

filetypes = (('XML files', '*.xml'), ('All files', '*.*'))
textofinal = list()

# Abrir archivo XML
try:
    docs = xml.dom.minidom.parse(yourfile)
except Exception as x:
    print("xml not found: ", x, "\ntry other file")
    exit()

def busca_archivo():

    messagebox.showinfo("Abir archivo XML",  "Seleccionar archivo")

def aviso():
    filename = filedialog.askopenfilename(
            title="Selecciona archivo Rocrail",
            filetypes=filetypes
            )
    global docs 
    docs = xml.dom.minidom.parse(filename)
    print(docs)


    print('Nombre del archivo ',  filename)

def get_plan():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")    
    items = docs.getElementsByTagName('plan')
    for idx, item in enumerate(items):
        roc_title = item.getAttribute('title')
        roc_pwd_ = item.getAttribute('rocrailpwd')
        roc_healthy = item.getAttribute('healthy')
        roc_scale = item.getAttribute('scale')
        roc_version= item.getAttribute('rocrailversion')
        roc_rocrailarch = item.getAttribute('rocrailarch')
        roc_OS= item.getAttribute('rocrailos')

        textofinal.append( 'Plan name: ' + roc_title
                    + '\nPath: ' + roc_pwd_  + '\nHealthy? ' + roc_healthy
                    + '\nScale: 1/'+ roc_scale + '\nVersion: ' + roc_version
                    + '\nArchitecture: ' + roc_rocrailarch + '\nOS: ' + roc_OS
                    )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])

def get_level():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")    
    items = docs.getElementsByTagName('zlevel')
    for idx, item in enumerate(items):
        lev_title = item.getAttribute('title')
        lev_tabid = item.getAttribute('tabidx')
        lev_symbolprefix = item.getAttribute('symbolprefix')
        
        textofinal.append( 'Level name: ' + lev_title
                        + '\nTab id: ' + lev_tabid + '\nSymbol prefix: '+ lev_symbolprefix
                        )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])

def get_tokens():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")
    items = docs.getElementsByTagName('tk')
    for idx, item in enumerate(items):
        token_name = item.getAttribute('id')
        token_type = item.getAttribute('type')
        token_ori = item.getAttribute('ori')
        token_x = item.getAttribute('x')
        token_y = item.getAttribute('y')
        token_z = item.getAttribute('z')

        textofinal.append( 'Item name: ' + token_name
                        + '\nType: ' + token_type + '\nOrientation: '+ token_ori
                        + '\nX axis: ' + token_x
                        + '\nY axis: ' + token_y
                        + '\nZ axis: ' + token_z
                        )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])

def get_desvios():
    global textofinal
    textofinal.clear()
    lista.delete(0, "end")

    items = docs.getElementsByTagName('sw')        
    for idx, item in enumerate(items):
            turn_name = item.getAttribute('id')
            turn_state = item.getAttribute('state')
            turn_delay = item.getAttribute('delay')
            turn_outoforder = item.getAttribute('outoforder')
            turn_type = item.getAttribute('type')
            turn_show = item.getAttribute('show')
            turn_ori = item.getAttribute('ori')
            turn_operable = item.getAttribute('operable')
            turn_savepos = item.getAttribute('savepos')
            turn_swtype = item.getAttribute('swtype')
            turn_addr1= item.getAttribute('addr1')
            turn_port1 = item.getAttribute('port1')
            turn_interface = item.getAttribute('iid')
            turn_frogaccessory = item.getAttribute('frogaccessory')
            turn_frogswitch = item.getAttribute('frogswitch')
            turn_froginvert = item.getAttribute('froginvert')
            turn_x = item.getAttribute('x')
            turn_y = item.getAttribute('y')
            turn_z = item.getAttribute('z')
            turn_desc = item.getAttribute('desc')
            
            textofinal.append( 'Turnout name: ' + turn_name
                     + '\nDescription: ' + turn_desc
                     + '\nType: ' + turn_type + '\nSaved position: ' +turn_savepos
                     + '\nSwitch type: ' + turn_swtype
                     + '\nState? ' + turn_state + '\nOut of order?: ' + turn_outoforder
                     + '\nShow? ' + turn_show + '\ndelay: ' + turn_delay + ' ms'
                     + '\nOrientation: '+ turn_ori
                     + '\nInterface: ' + turn_interface  + '\nOperable? ' + turn_operable + '\nAddress: ' + turn_addr1 + '\nPort: ' + turn_port1
                     + '\nFrog accesory? ' + turn_frogaccessory
                     + '\nFrog switch? ' + turn_frogswitch
                     + '\nFrog invert? ' + turn_froginvert
                     + '\nX axis: ' + turn_x
                     + '\nY axis: ' + turn_y
                     + '\nZ axis: ' + turn_z
                     )
            lista.insert(END, textofinal[idx].split('\n', 1)[0])
        
def get_texts():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")
    items = docs.getElementsByTagName('tx')
    for idx, item in enumerate(items):
        tx_name = item.getAttribute('id')
        tx_text = item.getAttribute('text')
        tx_block = item.getAttribute('block')
        tx_sliderval = item.getAttribute('sliderval')
        tx_ori = item.getAttribute('ori')
        tx_x = item.getAttribute('x')
        tx_y = item.getAttribute('y')
        tx_z = item.getAttribute('z')

        textofinal.append( 'Text name: ' + tx_name
                    + '\nText: ' + tx_text + '\nBlock: '+ tx_block
                    + '\nSliderval: '+ tx_sliderval
                    + '\nOrientation: ' + tx_ori
                    + '\nX axis: ' + tx_x + '\nY axis: ' + tx_y
                    + '\nZ axis: ' + tx_z
                    )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])

def get_block():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")
    items = docs.getElementsByTagName('bk')
    for idx, item in enumerate(items):
        bk_id = item.getAttribute('id')
        bk_desc = item.getAttribute('desc')
        bk_plat = item.getAttribute('platform')
        bk_state = item.getAttribute('state')
        bk_termst = item.getAttribute('terminalstation')
        bk_mainline = item.getAttribute('mainline')
        bk_signal = item.getAttribute('signal')
        bk_signalr = item.getAttribute('signalR')
        bk_witm = item.getAttribute('waitmode')
        bk_action = item.getAttribute('action')
        bk_resetsignalonexit = item.getAttribute('resetsignalonexit')

        textofinal.append( 'Block ID: ' + bk_id
            + '\nDescription: ' + bk_desc + '\nPlataform: '+ bk_plat
            + '\nState: ' + bk_state + '\nTerminal stataion? ' + bk_termst
            + '\nMain line? ' + bk_mainline + '\nSignal: '+ bk_signal
            + '\nSignalR: ' + bk_signalr + '\nReset signal on reset? ' + bk_resetsignalonexit
            + '\nWait mode: ' + bk_witm + '\nAction: ' + bk_action
            )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])
 
def get_signals():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")
    items = docs.getElementsByTagName('sg')
    for idx, item in enumerate(items):
        sig_name = item.getAttribute('id')
        sig_desc = item.getAttribute('desc')
        sig_interface = item.getAttribute('iid')
        sig_addr = item.getAttribute('addr1')
        sig_port = item.getAttribute('port1')              
        sig_type = item.getAttribute('type')
        sig_state = item.getAttribute('state')
        sig_ori = item.getAttribute('ori')
        sig_signal = item.getAttribute('signal')
        sig_aspects = item.getAttribute('aspects')
        sig_inv = item.getAttribute('inv')
    
        textofinal.append( 'Señales: ' + sig_name + '\nDescription: ' + sig_desc
                    + '\nInterface: ' + sig_interface + '\nAddress: ' + sig_addr
                    + '\tPort: ' + sig_port
                    + '\nType: ' + sig_type
                    + '\nSignal: '+ sig_signal  + '\nState: ' + sig_state
                    + '\nAspects: ' + sig_aspects + '\nOrientacion: '+ sig_ori
                    + '\nInvert? ' + sig_inv
                    )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])

def get_sensors():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")
    items = docs.getElementsByTagName('fb')
    for idx, item in enumerate(items):
        sen_name = item.getAttribute('id')
        sen_desc = item.getAttribute('desc')
        sen_interface = item.getAttribute('iid')
        sen_addr = item.getAttribute('addr')
        sen_state = item.getAttribute('state')
        sen_type = item.getAttribute('fbtype')
        sen_regtype = item.getAttribute('regtrigger')
        sen_block = item.getAttribute('blockid')
        sen_timer = item.getAttribute('timer')
        sen_counter = item.getAttribute('counter')
        sen_ori = item.getAttribute('ori')
        sen_road = item.getAttribute('road')
        sen_curve = item.getAttribute('curve')
        sen_interface = item.getAttribute('iid')
        sen_operable = item.getAttribute('operable')
    
        textofinal.append( 'Sensores: ' + sen_name + '\nDescription: ' + sen_desc
                    + '\nInterface: ' + sen_interface  + '\nAddress: ' + sen_addr
                    + '\nState? ' + sen_state + '\nType? ' + sen_type
                    + '\nRegister trigger: ' + sen_regtype
                    + '\nBlock: ' + sen_block  + '\nTimer: ' + sen_timer + ' x 100ms'
                    + '\ncontador: ' + sen_counter + '\nRoad? '+ sen_road
                    + '\nCurve? '+ sen_curve + '\nOrientacion: '+ sen_ori
                    + '\nOperable? ' + sen_operable
                    )
        lista.insert(END, textofinal[idx].split('\n', 1)[0])

def get_locomotoras():
    global textofinal
    textofinal.clear()

    lista.delete(0, "end")
    items = docs.getElementsByTagName('lc')
    for idx, item in enumerate(items):
        loc_name = item.getAttribute('id')
        loc_addr = item.getAttribute('addr')
        loc_spcnt = item.getAttribute('spcnt')
        loc_image = item.getAttribute('image')
        loc_number = item.getAttribute('number')
        loc_color = item.getAttribute('color')
        loc_show = item.getAttribute('show')
        loc_active = item.getAttribute('active')
        loc_schedule = item.getAttribute('usescheduletime')
        loc_vmin = item.getAttribute('V_min')
        loc_vmid = item.getAttribute('V_mid')
        loc_vcru = item.getAttribute('V_cru')
        loc_vmax = item.getAttribute('V_max')
        loc_engine = item.getAttribute('engine')
        loc_nejes = item.getAttribute("nraxis")
        loc_epoca = item.getAttribute("era")
        loc_descrip=item.getAttribute("desc")
        loc_interface=item.getAttribute("iid")

        textofinal.append( "Loc: " + loc_name
            + '\nInterface: '+ loc_interface + '\nNumber: ' +loc_number
            + '\tDCC:' + loc_addr + '\nSteeps:'+ loc_spcnt
            + '\nColor: ' + loc_color + '\nShow? ' + loc_show
            + '\nActive? ' + loc_active + '\nUse schedule time? ' + loc_schedule
            + '\nSpeeds: Vmin:'+ loc_vmin + '\tVmid:'+ loc_vmid + '\tVcru:'+ loc_vcru  + '\tVmax:'+ loc_vmax
            + '\nEngine:'+ loc_engine + "\nN. ejes: " + loc_nejes + "\nEpoca: " + loc_epoca
            + '\nImagen:'+ loc_image
            + '\nDescription:'+ loc_descrip)
        
        lista.insert(END, textofinal[idx].split('\n', 1)[0])


# Función para selección del Listbox "list"
def Select():
    global textofinal
    data = ''
    for i in lista.curselection():
        TextoSeleccion.config(state='normal')
        TextoSeleccion.delete(1.0, END)
        TextoSeleccion.insert(END,  textofinal[i])
        TextoSeleccion.config(state='disabled')
        #print("Seleccion" + listanombres)


# Crear interface Tkinter
root = Tk()
root.geometry("1100x450")
root.title("Listado Rocrail")

textoElemento = StringVar(value=" ")

#Menu
barramenu=Menu(root)
root.config(menu=barramenu,  width=1100,  height=400)

menuarchivo=Menu(barramenu,  tearoff=0 )
menuarchivo.add_command(label="abrir",  command=aviso)
barramenu.add_cascade(label="Archivo",  menu=menuarchivo)


#frame Botones root
framebt=Frame(root)
framebt.grid(row=0, column=1,  padx=2,  ipady=5, sticky='NS')

#frame Lista root
framels=Frame(root)
framels.grid(row=0, column=3, sticky='NS')


#texto en root
TextoSeleccion = Text(framels, padx=10, pady=10, bg="Black", fg="White",  font=('Courier', 12,  'bold'), width=50)

TextoSeleccion.grid(row=0, column=3, sticky='NS')

# Empieza lista
scroll = Scrollbar(framels, orient=VERTICAL)
scroll.grid(row=0,  column=2, sticky='NS')

lista = Listbox(framels, selectmode=SINGLE, bg="Black", fg="White", font=('Courier', 14,  'bold'), width=40, yscrollcommand=scroll.set)
scroll.config(command=lista.yview)
lista.bind('<<ListboxSelect>>', lambda x: Select())
lista.grid(row=0, column=1, sticky='NS')
# fin lista

# Empieza botones
btplan= Button(framebt,  text='Plan',  command=get_plan)
btplan.grid(row=0,  column=0,  sticky='EW')

btlevel = Button(framebt,  text='Level',  command=get_level)
btlevel.grid(row=1,  column=0,  sticky='EW')

btlocomotoras=Button(framebt,  text="Locomotive",  command=get_locomotoras)
btlocomotoras.grid(row=2,  column=0,  sticky='EW')

btdesvios=Button(framebt,  text="Turnout",  command=get_desvios)
btdesvios.grid(row=3,  column=0,  sticky='EW')

btvias=Button(framebt,  text="Traks", command=get_tokens)
btvias.grid(row=4,  column=0,  sticky='EW')

btsignals=Button(framebt,  text="Blocks",  command=get_block)
btsignals.grid(row=5,  column=0,  sticky='EW')

btsensores=Button(framebt,  text="Sensors",  command=get_sensors)
btsensores.grid(row=6,  column=0,  sticky='EW')

btsignals=Button(framebt,  text="Signals",  command=get_signals)
btsignals.grid(row=7,  column=0,  sticky='EW')

bttext=Button(framebt,  text="Texts",  command=get_texts)
bttext.grid(row=8,  column=0,  sticky='EW')
# Fin botones

root.mainloop()
