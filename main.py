from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        
        self.setWindowTitle('Text Redactor')
        self.setGeometry(400, 200, 560, 400)
        
        self.text_edit = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        
        self.current_file_path = None 
        self.createMenuBur()
     
    def createMenuBur(self):
        self.MenuBur = QMenuBar(self)
        self.setMenuBar(self.MenuBur)
        
        fileMenu = QMenu('&File', self)
        self.MenuBur.addMenu(fileMenu)
        
        editMenu = QMenu('&Edit', self)
        self.MenuBur.addMenu(editMenu)
        
        WindowMenu = QMenu('&Window', self)
        self.MenuBur.addMenu(WindowMenu)
        
        helpMenu = self.menuBar().addMenu('Help')
        self.MenuBur.addMenu(helpMenu)
        
        
        aboutAct = QAction('about', self)
        
        copyAct = QAction('Copy', self)
        copyAct.setShortcut('Ctrl+C')
        
        ctrlvAct = QAction('insert', self)
        ctrlvAct.setShortcut('Ctrl+V')
        
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

        open_act = QAction("Open", self)
        open_act.setShortcut('Ctrl+O')
        
        new_file_act = QAction("New file", self)
        new_file_act.setShortcut('Ctrl+N')
        
        save_act = QAction("Save", self)
        save_act.setShortcut('Ctrl+S')
        
        ctrlvAct.triggered.connect(self.action_click)
        open_act.triggered.connect(self.action_click)
        new_file_act.triggered.connect(self.action_click)
        save_act.triggered.connect(self.action_click)
        aboutAct.triggered.connect(self.action_click)
        copyAct.triggered.connect(self.action_click)
        
        editMenu.addAction(ctrlvAct)
        editMenu.addAction(copyAct)
        fileMenu.addAction(open_act)
        fileMenu.addAction(save_act)
        fileMenu.addAction(new_file_act)
        helpMenu.addAction(aboutAct)
        WindowMenu.addAction(exitAct)
        
        
    @QtCore.pyqtSlot()  
    def action_click(self):
        action = self.sender()
        if action.text() == "Open":
            try:
                fname = QFileDialog.getOpenFileName(self)[0]
                f = open(fname, 'r')
                with f:
                    data = f.read()
                    self.text_edit.setText(data)
                self.current_file_path = fname
                f.close
            except:
                
                self.error = QMessageBox()
                self.error.setWindowTitle('ERROR')
                self.error.setText('ERROR 404')
                self.error.setIcon(QMessageBox.Warning)
                self.error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                
                self.error.setInformativeText('you entered file incorrectly')
                
                self.error.exec_()
                
        elif action.text() == "New file":
            fname = QFileDialog.getSaveFileName(self)[0]
            try:
                f = open(fname, 'w')
                text = self.text_edit.toPlainText()
                f.write(text)
                f.close
                
            except:
                self.error = QMessageBox()
                self.error.setWindowTitle('ERROR')
                self.error.setText('ERROR 404')
                self.error.setIcon(QMessageBox.Warning)
                self.error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                
                self.error.setInformativeText('you entered file incorrectly')
                
                self.error.exec_()
            
        elif action.text() == "Save":
            if self.current_file_path:
                try:
                    icon = QPixmap('check.png')
                    with open(self.current_file_path, 'w') as file:
                        file.write(self.text_edit.toPlainText())
                    self.file_seved = QMessageBox()
                    self.file_seved.setFixedSize(400, 200)
                    self.file_seved.setWindowTitle('FILE Maneger')
                    self.file_seved.setText('File saved')
                    new_size = icon.scaled(50, 50)
                    self.file_seved.setIconPixmap(new_size)
                    self.file_seved.setDefaultButton(QMessageBox.Ok)
                    self.file_seved.exec_()
                    
                except Exception as e:
                    print(e)
                    self.error = QMessageBox()
                    self.error.setWindowTitle('ERROR')
                    self.error.setText('ERROR 404')
                    self.error.setIcon(QMessageBox.Warning)
                    self.error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    
                    self.error.setInformativeText('Ошибка сохранения файла!')
                    self.error.setGeometry(400, 250, 400, 250)
                    self.error.exec_()
        
        elif action.text() == 'about':
            
            self.about = QMessageBox()
            self.about.setWindowTitle('About app')
            self.about.setText('About me')
            self.about.setIcon(QMessageBox.Information) 
            self.about.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            self.about.setInformativeText('Привет, Я разработчик этой программы \n Она была разработана для обучение PyQt5')
            self.about.resize(self.about.sizeHint())
            self.about.exec_()
        
        elif action.text() == 'Copy':
            cursor = self.text_edit.textCursor()
            selected_text = cursor.selectedText()
            if selected_text:
                QApplication.clipboard().setText(selected_text)

        elif action.text() == 'insert':
            cursor = self.text_edit.textCursor()
            cursor.insertText(QApplication.clipboard().text())

            
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle('ERROR')
            self.error.setText('ERROR 404')
            self.error.setIcon(QMessageBox.Warning)
            self.error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
               
            self.error.setInformativeText('you entered file incorrectly')
                
            self.error.exec_()
                             
            
def application():
    app = QApplication(sys.argv)
    window = Window()
    
    
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    application()
        