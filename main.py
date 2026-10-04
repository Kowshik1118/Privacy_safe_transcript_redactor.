import re, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinter import ttk
BG='#0A1020'; CARD='#141E34'; TEXT='#F3F6FF'; MUTED='#AAB7D0'; BLUE='#668CFF'; TEAL='#3DDBBD'; RED='#FF6D80'
PATTERNS=[
 ('Email',r'(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+(?![\w.+-])'),
 ('Phone',r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)'),
 ('Card',r'(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)'),
 ('Aadhaar-like ID',r'(?<!\d)\d{4}[ -]?\d{4}[ -]?\d{4}(?!\d)'),
 ('PAN-like ID',r'(?<![A-Z])[A-Z]{5}\d{4}[A-Z](?![A-Z])'),
 ('IP address',r'(?<![\d.])(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![\d.])'),
 ('URL',r'https?://[^\s<>"\]]+'),
 ('Date of birth',r'(?<!\d)(?:0?[1-9]|[12]\d|3[01])[/-](?:0?[1-9]|1[0-2])[/-](?:19|20)\d{2}(?!\d)')]
def redact(text, enabled):
 counts={}; n=0
 for label,pat in PATTERNS:
  if label not in enabled:continue
  i=0
  def repl(m):
   nonlocal i,n;i+=1;n+=1;return f'[{label.upper().replace(" ","_")}_{i}]'
  text=re.sub(pat,repl,text,flags=re.I);counts[label]=i
 return text,counts,n
class App(tk.Tk):
 def __init__(self):
  super().__init__();self.title('PrivateText — Local Transcript Redactor');self.geometry('1160x730');self.minsize(930,600);self.configure(bg=BG);self.vars={};self.build()
 def L(self,p,t,size=11,c=TEXT,b=False,**kw):return tk.Label(p,text=t,bg=p['bg'],fg=c,font=('Segoe UI',size,'bold' if b else 'normal'),**kw)
 def card(self,p):return tk.Frame(p,bg=CARD,highlightthickness=1,highlightbackground='#263654')
 def build(self):
  h=tk.Frame(self,bg=BG);h.pack(fill='x',padx=36,pady=(25,10));self.L(h,'PRIVATETEXT',12,TEAL,True).pack(anchor='w');self.L(h,'Privacy-safe transcript redactor',27,TEXT,True).pack(anchor='w');self.L(h,'Offline masking • no API • no server • no database • nothing is uploaded',11,MUTED).pack(anchor='w',pady=(3,0))
  outer=tk.Frame(self,bg=BG);outer.pack(fill='both',expand=True,padx=36,pady=12);outer.columnconfigure(0,weight=1);outer.columnconfigure(1,weight=1);outer.rowconfigure(0,weight=1)
  a=self.card(outer);a.grid(row=0,column=0,sticky='nsew',padx=(0,8));b=self.card(outer);b.grid(row=0,column=1,sticky='nsew',padx=(8,0))
  self.L(a,'ORIGINAL TRANSCRIPT',11,MUTED,True).pack(anchor='w',padx=18,pady=(16,7));self.source=tk.Text(a,bg='#0D182C',fg=TEXT,insertbackground=TEXT,relief='flat',wrap='word',font=('Segoe UI',11),padx=12,pady=12);self.source.pack(fill='both',expand=True,padx=18);self.source.insert('1.0','Call from Ravi Kumar, phone +91 9876543210. Email ravi@example.com. Please send details to https://example.com/support.')
  row=tk.Frame(a,bg=CARD);row.pack(fill='x',padx=18,pady=14);tk.Button(row,text='Open .txt',command=self.open,bg=BLUE,fg='white',relief='flat',font=('Segoe UI',10,'bold'),padx=13,pady=7).pack(side='left');tk.Button(row,text='Redact locally',command=self.run,bg=TEAL,fg='#06141A',relief='flat',font=('Segoe UI',10,'bold'),padx=13,pady=7).pack(side='right')
  self.L(b,'REDACTED TRANSCRIPT',11,MUTED,True).pack(anchor='w',padx=18,pady=(16,7));self.dest=tk.Text(b,bg='#0D182C',fg=TEXT,relief='flat',wrap='word',font=('Segoe UI',11),padx=12,pady=12);self.dest.pack(fill='both',expand=True,padx=18);self.dest.config(state='disabled')
  r=tk.Frame(b,bg=CARD);r.pack(fill='x',padx=18,pady=14);self.summary=self.L(r,'Ready',10,MUTED);self.summary.pack(side='left');tk.Button(r,text='Save redacted .txt',command=self.save,bg=BLUE,fg='white',relief='flat',font=('Segoe UI',10,'bold'),padx=13,pady=7).pack(side='right')
  opt=self.card(self);opt.pack(fill='x',padx=36,pady=(0,25));self.L(opt,'MASKING RULES',10,MUTED,True).pack(anchor='w',padx=18,pady=(12,4));rr=tk.Frame(opt,bg=CARD);rr.pack(fill='x',padx=12,pady=(0,10))
  for label,_ in PATTERNS:
   v=tk.BooleanVar(value=True);self.vars[label]=v;tk.Checkbutton(rr,text=label,variable=v,bg=CARD,fg=TEXT,selectcolor='#233858',activebackground=CARD,activeforeground=TEXT,font=('Segoe UI',10)).pack(side='left',padx=7)
 def open(self):
  p=filedialog.askopenfilename(filetypes=[('Text files','*.txt'),('All files','*.*')])
  if p:
   try:self.source.delete('1.0','end');self.source.insert('1.0',Path(p).read_text(encoding='utf-8'))
   except Exception as e:messagebox.showerror('Cannot open file',str(e))
 def run(self):
  out,c,n=redact(self.source.get('1.0','end-1c'),{k for k,v in self.vars.items() if v.get()});self.dest.config(state='normal');self.dest.delete('1.0','end');self.dest.insert('1.0',out);self.dest.config(state='disabled');details=', '.join(f'{k}: {v}' for k,v in c.items() if v) or 'No configured identifiers detected';self.summary.config(text=f'{n} item(s) masked • {details}')
 def save(self):
  data=self.dest.get('1.0','end-1c')
  if not data: return messagebox.showinfo('Nothing to save','Redact a transcript first.')
  p=filedialog.asksaveasfilename(defaultextension='.txt',initialfile='redacted_transcript.txt',filetypes=[('Text files','*.txt')])
  if p:
   try:Path(p).write_text(data,encoding='utf-8');messagebox.showinfo('Saved','Redacted file saved locally.')
   except Exception as e:messagebox.showerror('Cannot save file',str(e))
if __name__=='__main__':App().mainloop()
