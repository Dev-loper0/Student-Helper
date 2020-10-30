from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.list import ThreeLineListItem,BaseListItem
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Color

import datetime
import json
import win32ui
import xlwt

class HybridListBaseItme(FloatLayout):
	def __init__(self,examp,tp_p,tp_coff,td_p,td_coff,exam_coff,**kwargs):
		super().__init__(**kwargs)
		self.height = dp(48)
		self.ids.exam_p.text = examp
		self.ids.tp_p.text = tp_p
		self.ids.tp_coff.text = tp_coff
		self.ids.td_p.text = td_p
		self.ids.td_coff.text = td_coff
		self.ids.exam_coff.text = exam_coff
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			self.canvas.children[0].rgba = (.8,.8,.8,1)
	def on_touch_up(self,touch):
		if self.collide_point(*touch.pos):
			self.canvas.children[0].rgba = (0,0,0,0)
class Show_m(BaseDialog):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
class Point_data(BaseDialog):
	def __init__(self,calculator,**kwargs):
		super().__init__(**kwargs)
		self.calculator = calculator
	def remove_item(self):
		self.calculator.remove_item()
		self.dismiss()
	def save_point(self):
		self.calculator.save_point()
		self.dismiss()
class Add_point_data(BaseDialog):
	def __init__(self,calculator,**kwargs):
		super().__init__(**kwargs)
		self.calculator = calculator
	def add_point(self,examp,tp_p,tp_coff,td_p,td_coff,exam_coff):
		if examp != "" and tp_p != "" and tp_coff != "" and td_p != "" and td_coff != "" and exam_coff != "":
			new_point = HybridListBaseItme(examp,tp_p,tp_coff,td_p,td_coff,exam_coff)
			new_point.bind(on_touch_up=self.calculator.show_item_data)
			self.calculator.ids.points_list.add_widget(new_point)
			self.dismiss()
		else:
			self.calculator.show_m.ids.lab.text = "Please Fill All Text Fildes"
			self.calculator.show_m.open()
class Calculator(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.add_point_data = Add_point_data(self)
		self.point_data = Point_data(self)
		self.show_m = Show_m()
		self.edited = True
	def show_item_data(self,item,touch):
		if item.collide_point(*touch.pos):
			self.item = item
			self.point_data.ids.exam_p.text = item.ids.exam_p.text
			self.point_data.ids.tp_p.text = item.ids.tp_p.text
			self.point_data.ids.tp_coff.text = item.ids.tp_coff.text
			self.point_data.ids.td_p.text = item.ids.td_p.text
			self.point_data.ids.td_coff.text = item.ids.td_coff.text
			self.point_data.ids.exam_coff.text = item.ids.exam_coff.text
			self.point_data.open()
	def remove_item(self):
		if self.item != None:
			self.ids.points_list.remove_widget(self.item)
	def save_point(self):
		if self.item != None:
			self.item.ids.exam_p.text = self.point_data.ids.exam_p.text
			self.item.ids.tp_p.text = self.point_data.ids.tp_p.text
			self.item.ids.tp_coff.text = self.point_data.ids.tp_coff.text
			self.item.ids.td_p.text = self.point_data.ids.td_p.text
			self.item.ids.td_coff.text = self.point_data.ids.td_coff.text
			self.item.ids.exam_coff.text = self.point_data.ids.exam_coff.text
	def Calculate(self):
		if len(self.ids.points_list.children) > 0:
			m = 0
			coffs = 0
			for childe in self.ids.points_list.children:
				# ((exam + td_p / td_coff)+(tp_p/tp_coff))*exam_coff
				mp = (((float(childe.ids.exam_p.text)+float(childe.ids.td_p.text))/float(childe.ids.td_coff.text))+\
				(float(childe.ids.tp_p.text)/float(childe.ids.tp_coff.text)))*float(childe.ids.exam_coff.text)
				coffs += float(childe.ids.exam_coff.text)
				m += mp
			m = m / coffs
			self.show_m.ids.lab.text = f"Your Point is : {m}"
			self.show_m.open()
		else:
			self.show_m.ids.lab.text = "Please Insert All Points !"
			self.show_m.open()
	def save_as_xlsx(self):
		f_cols = ["Exam","Tp","Tp coff","Td","Td coff","Exam Coff"]
		o = win32ui.CreateFileDialog( 1, ".xls", "Points.xls", 0,\
				 "Text Files (*.xls)|*.xls|All Files (*.*)|*.*|")
		o.DoModal()
		path = o.GetPathName()
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Sheet')
		for index in range(len(f_cols)):
			ws.write(0, index, f_cols[index])
		self.ids.points_list.children.reverse()
		for row in range(len(self.ids.points_list.children)):
			childe = self.ids.points_list.children[row]
			childe.children[0].children.reverse()
			for col in range(len(childe.ids)):
				childes = childe.children[0].children[col]
				ws.write(row+1, col, float(childes.text))
		wb.save(path)
class Item_data(BaseDialog):
	def __init__(self,todo,**kwargs):
		super().__init__(**kwargs)
		self.todo = todo
	def remove_item(self):
		self.todo.remove_item()
		self.dismiss()
class Add_Note_Dialog(BaseDialog):
	def __init__(self,todo,**kwargs):
		super().__init__(**kwargs)
		self.todo = todo
	def add_note(self,title,description):
		now = str(datetime.datetime.now())
		new_item = ThreeLineListItem(id=str(self.todo.id_count),text=title,secondary_text=description,tertiary_text=now)
		new_item.bind(on_release=self.todo.show_item_data)
		self.todo.ids.todolist.add_widget(new_item)
		self.todo.save_todo_list(title,description,now)
		self.dismiss()
class Todo(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.add_note_dia = Add_Note_Dialog(self)
		self.item_data_dia = Item_data(self)
		self.id_count = 0
	def load_todo_list(self):
		with open("assest/todo_list.json","r") as td:
			self.todos = json.load(td)
			for todo in self.todos:
				title = self.todos[todo]['title']
				description = self.todos[todo]['description']
				now = self.todos[todo]['date']
				new_item = ThreeLineListItem(id=str(self.id_count),text=title,secondary_text=description,tertiary_text=now)
				new_item.bind(on_release=self.show_item_data)
				self.ids.todolist.add_widget(new_item)
				self.id_count += 1
	def save_todo_list(self,title,description,now):
		data = {f"{len(self.todos)}":{"title":title,"description":description,"date":now}}
		self.todos.update(data)
		self.write()
	def show_item_data(self,item):
		self.item = item
		self.item_data_dia.open()
		self.item_data_dia.ids.title.text = item.text
		self.item_data_dia.ids.time_set.text = item.tertiary_text
		self.item_data_dia.ids.description.text = item.secondary_text
	def remove_item(self):
		if self.item != None:
			self.ids.todolist.remove_widget(self.item)
			self.todos.pop(self.item.id)
			self.id_count -= 1
			self.write()
	def write(self):
		with open("assest/todo_list.json","w") as td:
			json.dump(self.todos,td)
class Node(FloatLayout):
	def __init__(self,p,**kwargs):
		super().__init__(**kwargs)
		self.p = p
		self.sel = False
		self.lines = []
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			if not self.sel:
				self.sel = True
				with self.canvas:
					Color(0,0,0)
					line = Line(rectangle=(self.x-5,self.y-5,
						self.width+10,self.height+10),
						dash_length=5,dash_offset=2)
					self.lines.append(line)
				self.p.sel = self
				self.p.ids.text_inp.text = self.ids.Lab.text
				self.p.ids.size_inp.text = str(self.size)
				self.p.ids.color_inp.text = "Red"
		else:
			if self.sel:
				self.canvas.remove(self.lines[0])
				self.lines = []
				self.sel = False
	def on_touch_move(self,touch):
		if self.sel:
	 		self.center = touch.pos
	 		self.lines[0].rectangle=(self.x-5,self.y-5,
						self.width+10,self.height+10)
	def Update(self):
		self.ids.Lab.text = self.p.ids.text_inp.text
		self.ids.size = self.p.ids.size_inp.text
	def on_touch_up(self,touch):
		pass
class MindMap(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.lines = []
		self.sel = None
	def Add_root_node(self):
		self.node = Node(self,size_hint=(None,None),size=(150,150),pos=(0,150))
		for child in self.ids.node_scene.children:
			if self.node.collide_point(self.node.pos[0],self.node.pos[1]):
				self.node.pos[0] = self.ids.node_scene.children[0].pos[0] + 200#self.node.pos[0] 
				self.node.pos[1] = self.node.pos[1] #self.ids.node_scene.children[0].pos[1]
		self.ids.node_scene.add_widget(self.node)
	def Add_child_node(self):
		child_node = Node(self,size_hint=(None,None),size=(75,75),pos=(self.node.pos[0]+200,50))
		for child in self.ids.node_scene.children:
			if child_node.collide_point(child.pos[0],child.pos[1]):
				child_node.pos[0] = child_node.pos[0]
				child_node.pos[1] =  self.ids.node_scene.children[0].pos[1] + 100
		with self.ids.node_scene.canvas:
			Color(0,0,0)
			l = Line(points=[[self.node.center[0]+ self.node.size[0] /2 ,self.node.center[1]],
						[child_node.center[0] - child_node.size[0]/2,child_node.center[1]]])
			self.lines.append(l)
		self.ids.node_scene.add_widget(child_node)
	def Update(self):
		if self.sel != None:
			self.sel.Update()
	def Clear(self):
		self.ids.node_scene.clear_widgets()
		for line in self.lines:
			self.ids.node_scene.canvas.remove(line)
		self.lines = []
class StdApp(MDApp):
	def __init__(self,**kwargs):
		self.title = "Student App"
		self.theme_cls.primary_palette = "Blue"
		super().__init__(**kwargs)
if __name__ == '__main__':
	StdApp().run()