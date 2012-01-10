'''
Created on 23/12/2011

@author: pantonio
'''

from tkinter import tix
import tkinter
#import tkinter.ttk

class App:
	def __init__(self, master, proc_fn):
		self.master = master
		self.frame = tix.Frame(master)
		self.frame.rowconfigure(0, minsize=15)
		self.frame.rowconfigure(3, minsize=15)
		self.frame.rowconfigure(5, minsize=15)
		self.frame.rowconfigure(7, minsize=15)
		self.frame.columnconfigure(0, minsize=15)
		self.frame.columnconfigure(4, minsize=15)
		self.frame.pack()
		
		tix.Label(self.frame, text="Archivo de Entrada :").grid(row=2,sticky=tix.W)
		tix.Label(self.frame, text="Archivo de Salida  :").grid(row=4,sticky=tix.W)
		
		self.input = tix.Entry(self.frame)
		self.input.grid(row=2, column=3)
		tix.Button(self.frame, text="...", command=self.get_input).grid(row=2, column=2)
		self.output=tix.Entry(self.frame)
		self.output.grid(row=4, column=3)
		tix.Button(self.frame, text="...", command=self.set_output).grid(row=4, column=2)
		
		tix.Button(self.frame, text="Cancelar", command=self.frame.quit).grid(row=6, column=1)
		tix.Button(self.frame, text="Procesar", command=proc_fn).grid(row=6, column=3)
		
		self.box = None
		self.in_out_state = None
		self.ready = False
		self.in_file = None
		self.out_file =None

	def file_select_ok(self):
		if self.box is not None:
			w = self.box.subwidget('file')
			w1 = w.subwidget('entry')
			file = w1.get()
			w = self.box.subwidget('dir')
			w1= w.subwidget('entry')
			path=w1.get()
			if self.in_out_state == 'IN':
				self.input.delete(0, tkinter.END)
				self.input.insert(0, path + '/' + file)
			elif self.in_out_state == 'OUT':
				self.output.delete(0, tkinter.END)
				self.output.insert(0, path + '/' + file)
			self.box.destroy()
			self.in_out_state = None
		
	def file_selection(self):
		self.box = tix.ExFileSelectBox(self.master)
		
		w = self.box.subwidget('cancel')
		w['command']=self.box.destroy
		
		w = self.box.subwidget('ok')
		w['command']=self.file_select_ok
		
		'''
		self.subwidget_list['cancel'] = _dummyButton(self, 'cancel')
		self.subwidget_list['ok'] = _dummyButton(self, 'ok')
		self.subwidget_list['hidden'] = _dummyCheckbutton(self, 'hidden')
		self.subwidget_list['types'] = _dummyComboBox(self, 'types')
		self.subwidget_list['dir'] = _dummyComboBox(self, 'dir')
		self.subwidget_list['dirlist'] = _dummyDirList(self, 'dirlist')
		self.subwidget_list['file'] = _dummyComboBox(self, 'file')
		self.subwidget_list['filelist'] = _dummyScrolledListBox(self, 'filelist')

		'''
		self.box.pack()
		
	def get_input(self):
		self.in_out_state = 'IN'
		self.file_selection()
		
	def set_output(self):
		self.in_out_state = 'OUT'
		self.file_selection()

	def ok_to_proc(self):
		self.ready = True
		self.in_file = self.input.get()
		self.out_file = self.output.get()
		self.frame.destroy()
		
	def get_file1(self):
		return self.input.get()
	
	def get_file2(self):
		return self.output.get()
	
	def say_hi(self ):
		print("Hi " + self.input.get() + " living at " + self.output.get())


