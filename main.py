from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mysql.connector as mdb
import sys


MainUI,_ = loadUiType("data/main.ui")


class Main(QMainWindow, MainUI):
	def __init__(self, parent=None):
		super(Main, self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.Change_UI()
		self.HandelButtons()

	def Change_UI(self):
		style = open('data/themes/default_css.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

		header = self.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(2, QHeaderView.Stretch)
		header.setSectionResizeMode(3, QHeaderView.Stretch)
		header.setSectionResizeMode(4, QHeaderView.Stretch)

		# connect_to_db
		self.ConnectToDb()
		self.GetData()

	def ClearFields(self):
		# clear fields
		first_name = self.first_name.clear()
		last_name = self.last_name.clear()
		email_addr = self.email_address.clear()
		home_addr = self.address.clear()
		origin = self.origin.clear()

		first_name = self.first_name_2.clear()
		last_name = self.last_name_2.clear()
		email_addr = self.email_address_2.clear()
		home_addr = self.address_2.clear()
		origin = self.origin_2.clear()



	def ConnectToDb(self):
		self.conn = mdb.connect(host="localhost", user="root", password="toor", database="youtube_tutorial")
		self.cursor = self.conn.cursor()


	def GetData(self):
		sql = """ SELECT first_name, last_name, email, home_addr, origin, person_id FROM profiles """
		self.cursor.execute(sql)
		result = self.cursor.fetchall()

		self.tableWidget.setRowCount(0)

		for row_num, row_data in enumerate(result):
			self.tableWidget.insertRow(row_num)
			for column_num, data in enumerate(row_data):
				self.tableWidget.setItem(row_num, column_num, QTableWidgetItem(str(data)))

	def HandelButtons(self):
		self.btn_submit.clicked.connect(self.SubmitProfile)
		self.btn_update.clicked.connect(self.UpdateProfile)
		self.btn_delete.clicked.connect(self.DeleteProfile)
		self.btn_search.clicked.connect(self.SearchProfile)


	def SearchProfile(self):
		id_ = self.id_edit.text()
		sql = """ SELECT  first_name, last_name, email, home_addr, origin FROM profiles WHERE person_id=%s """
		data = (id_,)
		self.cursor.execute(sql, data)
		result = self.cursor.fetchone()

		first_name = self.first_name_2.setText(result[0])
		last_name = self.last_name_2.setText(result[1])
		email_addr = self.email_address_2.setText(result[2])
		home_addr = self.address_2.setText(result[3])
		origin = self.origin_2.setText(result[4])

	def DeleteProfile(self):
		id_ = self.id_edit.text()
		sql = """ DELETE FROM profiles WHERE person_id=%s """
		data = (id_,)
		self.cursor.execute(sql, data)
		self.conn.commit()

		self.ClearFields()

	def SubmitProfile(self):
		first_name = self.first_name.text()
		last_name = self.last_name.text()
		email_addr = self.email_address.text()
		home_addr = self.address.text()
		origin = self.origin.text()

		# mysql query
		sql = """ INSERT INTO profiles (first_name, last_name, email, home_addr, origin) 
				VALUES (%s, %s, %s, %s, %s)"""
		data = (str(first_name), str(last_name), str(email_addr), str(home_addr), str(origin))
		self.cursor.execute(sql, data)
		self.conn.commit()

		# getting the data from the database
		self.GetData()
		self.ClearFields()

	def UpdateProfile(self):
		id_ = self.id_edit.text()
		first_name = self.first_name_2.text()
		last_name = self.last_name_2.text()
		email_addr = self.email_address_2.text()
		home_addr = self.address_2.text()
		origin = self.origin_2.text()

		sql = """ UPDATE profiles SET first_name=%s, last_name=%s, email=%s, home_addr=%s, origin=%s WHERE person_id=%s"""
		data = (str(first_name), str(last_name), str(email_addr), str(home_addr), str(origin), str(id_))

		self.cursor.execute(sql, data)
		self.conn.commit()

		# getting data
		self.GetData()
		self.ClearFields()



	def Dark_Blue_Theme(self):
		style = open('data/themes/darkblue.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Gray_Theme(self):
		style = open('data/themes/darkgray.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Orange_Theme(self):
		style = open('data/themes/darkorange.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	def QDark_Theme(self):
		style = open('data/themes/qdark.css' , 'r')
		style = style.read()
		self.setStyleSheet(style)

	


def main():
	app = QApplication(sys.argv)
	window = Main()
	window.show()
	app.exec_()

if __name__ == "__main__":
	main()








