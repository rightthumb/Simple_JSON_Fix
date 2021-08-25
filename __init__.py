

from os import path
class Simple_JSON_Fix:
	def __init__( self, path_or_code, i=0, save=False ):
		self.json={}
		self.index={}
		self.json = {}
		if path.isfile(path_or_code):
			with open( path_or_code, 'r' ) as file:
				self.asset = file.read()
		else:
			self.asset = path_or_code

		while self.asset.startswith(' ') or self.asset.startswith('\t'):
			self.asset=self.asset[1:]
		# print('self.asset',self.asset)
		code=self.asset
		self.index = self.vindex(self.asset,i)
		# print(self.index)

		# for o in index:
		# 	c=index[o]
		# 	# print(o,c,type(self.asset))
		# 	print( self.asset[o:c+1] )


		loop=0
		while loop < 4 and not i in self.index:
			self.asset.replace('\t','    ')
			while '\n ' in self.asset:
				self.asset=self.asset.replace('\n ','\n')
			while ' \n' in self.asset:
				self.asset=self.asset.replace(' \n','\n')
			self.asset=self.asset.replace('\n','')

			loop+=1
			probable_1 = self.find_all(self.asset,'}}')
			if probable_1:
				probable_1.reverse()
				a=self.asset[i:probable_1[0]]
				b=self.asset[probable_1[0]+1:len(self.asset)]
				self.asset=a+b
				self.index=self.vindex(self.asset,i)

		if not i in self.index:
			self.asset=code
			while loop < 10 and not i in self.index:
				loop+=1
				self.asset+='}'
				self.index=self.vindex(self.asset,i)
		if not i in self.index:
			self.asset=code
			while loop < 10 and not i in self.index:
				loop+=1
				self.asset='{'+self.asset
				self.index=self.vindex(self.asset,i)
		if not i in self.index:
			self.asset=code
		self.json=self.variable()



		if save and path.isfile(path_or_code):
			import simplejson
			f = open(path_or_code,'w')
			f.write(str(simplejson.dumps(self.json, indent=4, sort_keys=False)))
			f.close()


	def vindex( self, code, i=0, esc='\\', n='' ):
		at=i

		table_brackets = {}
		table_brackets['i']=0
		table_brackets['open'] = {}

		table_braces = {}
		table_braces['i']=0
		table_braces['open'] = {}

		table_par = {}
		table_par['i']=0
		table_par['open'] = {}



		index={}

		i-=1
		while True:
			i+=1
			if i >= len(code):
				break
			c=code[i]
			try:
				c2=c+code[i+1]
			except Exception as e:
				c2=''
			try:
				c3=c2+code[i+2]
			except Exception as e:
				c3=''
			try:
				c4=c3+code[i+3]
			except Exception as e:
				c4=''
			try:
				c5=c4+code[i+4]
			except Exception as e:
				c5=''


			if len(esc) == 1 and c==esc:
				i+=1
			elif len(n) == 1 and c==n:
				return i
			elif len(n) == 2 and c2==n:
				return i+1
			elif len(n) == 3 and c3==n:
				return i+2
			elif not n and c in '0123456789.':
				cx = c
				ii=i-1
				while cx in '0123456789.':
					ii+=1
					cx=code[ii]
				index[i] = ii-1
				i=index[i]
			elif not n and c in '\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
				cx = c
				ii=i-1
				# while cx in '*+?\\.^$&|/{[]()}-,^'+'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._':
				while cx in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._':
					ii+=1
					cx=code[ii]
				index[i] = ii-1
				i=index[i]
			elif not n and c3 == '"""':
				index[i] = self.vindex(code,i+3,esc,n='"""')
				i=index[i]
			elif not n and c3 == "'''":
				index[i] = self.vindex(code,i+3,esc,n="'''")
				i=index[i]
			elif not n and c == "'":
				index[i] = self.vindex(code,i+1,esc,n="'")
				i=index[i]
			elif not n and c == '"':
				index[i] = self.vindex(code,i+1,esc,n='"')
				i=index[i]
			elif not n and c2 == '/*':
				i = self.vindex(code,i+2,esc,n='*/')
			elif not n and c2 == '//':
				i = self.vindex(code,i+2,esc,n='\n')


			elif not n and c == '{':
				table_brackets['i']+=1
				table_brackets['open'][table_brackets['i']]=i
			elif not n and c == '}':
				s=table_brackets['open'][table_brackets['i']]
				index[ s ]=i
				table_brackets['i']-=1
				if s==at:
					return index
			elif not n and c == '[':
				table_braces['i']+=1
				table_braces['open'][table_braces['i']]=i
			elif not n and c == ']':
				s=table_braces['open'][table_braces['i']]
				index[ s ]=i
				table_braces['i']-=1
				if s==at:
					return index
			elif not n and c == '(':
				table_par['i']+=1
				table_par['open'][table_par['i']]=i
			elif not n and c == ')':
				s=table_par['open'][table_par['i']]
				index[ s ]=i
				table_par['i']-=1
				if s==at:
					return index
		return index


	def genJson_rec( self, dic ):

		n = {}
		for k in dic:
			n[k] = dic[k]
		self.json_records.append(n)


	def variable( self ):
		self.json_records = []
		def getData(o,c,f=None, p=[],v={}, l=None, spent=[], rec=[], top=True, li=[]):
			oo = o
			cc = c

			while oo < c :
				if oo in spent:
					oo+=1
				spent.append(oo)
				if oo in self.index:
					
					cc = self.index[oo]
					txt=self.asset[oo:cc+1]
					# print(txt)
					txtl=txt.lower()
					if txt.startswith('"') or txt.startswith('"'):
						txtq=txt[1:-1]
					else:
						txtq=txt
					
					if txt.startswith('['):
						if not f is None:
							z2 = getData(oo,cc,f=None, p=[],v={}, l=None, spent=spent, rec=[], top=True, li=[])
							v[f] = z2
						else:
							vx = getData(oo,cc,f=None, p=[],v={}, l=None, spent=spent, rec=rec, top=False, li=li)
						f = None
					elif txt.startswith('{'):
						if not f is None:
							z2 = getData(oo,cc,f=None, p=[],v={}, l=None, spent=spent, rec=rec, top=True, li=li)
							v[f] = z2
						else:
							vy = getData( oo, cc, None, p, {}, l, spent, rec, False, li )
							self.genJson_rec(vy)
						f = None
					elif txt and txt[0] in '"':
						li.append(txtq)

						if self.asset[o] == '{':
							if f is None:
								f = txtq
								p.append(f)
							else:
								v[f] = txtq
								f = None


					elif txt and txt[0] in '0123456789.-':
						if '.' in txt:
							xx = float(txt)
						else:
							xx = int(txt)
						li.append(xx)
						v[f] = xx
						f = None

					elif txtl.lower().startswith('true'):
						li.append(True)
						v[f] = True
						f = None
					elif txtl.lower().startswith('false'):
						li.append(False)
						v[f] = False
						f = None
					elif txtl.lower().startswith('null'):
						li.append(None)
						v[f] = None
						f = None
					oo = cc


				oo+=1
			if top:
				if self.asset[o] == '[':
					if self.json_records:
						return self.json_records
					else:
						return li
				else:
					if len(self.json_records) > 1:
						return self.json_records
					if self.json_records:
						return self.json_records[0]
					return v
			if self.asset[o] == '[':
				return li
			return v
			if self.asset[o] == '{':
				return v

		o = 0
		c = len(self.asset)-1
		ss = getData(o,c)
		self.json=ss
		return ss

	def find_all( self, string, sub ):
		def find_all_run( string, sub ):
			s = 0
			while True:
				s = string.find(sub, s)
				if s == -1: return
				yield s
				s += len(sub)
		return list(find_all_run(string, sub))



# test=Simple_JSON_Fix( 'file.json', save=True )
# python_dic=test.json