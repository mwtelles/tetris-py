import sys
import random
from utils import *
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHBoxLayout, QLabel


class TetrisGame(QMainWindow):
	def __init__(self):
		super().__init__()

		self.is_paused = False

		self.is_started = False
		self.initUI()

	def initUI(self):

		self.grid_size = 22

		self.fps = 200
		self.timer = QBasicTimer()

		self.setFocusPolicy(Qt.StrongFocus)

		layout_horizontal = QHBoxLayout()
		self.inner_board = InnerBoard()
		self.external_board = ExternalBoard(self, self.grid_size, self.inner_board)
		layout_horizontal.addWidget(self.external_board)
		self.side_panel = SidePanel(self, self.grid_size, self.inner_board)
		layout_horizontal.addWidget(self.side_panel)
		self.status_bar = self.statusBar()
		self.external_board.score_signal[str].connect(self.status_bar.showMessage)
		self.start()
		self.center()
		self.setWindowTitle('Tetris- github/mwtelles')
		self.show()
		self.setFixedSize(self.external_board.width() + self.side_panel.width(),
						  self.side_panel.height() + self.status_bar.height())

	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

	def updateWindow(self):
		self.external_board.updateData()
		self.side_panel.updateData()
		self.update()

	def start(self):
		if self.is_started:
			return
		self.is_started = True
		self.inner_board.createNewTetris()
		self.timer.start(self.fps, self)

	def pause(self):
		if not self.is_started:
			return
		self.is_paused = not self.is_paused
		if self.is_paused:
			self.timer.stop()
			self.external_board.score_signal.emit('Paused')
		else:
			self.timer.start(self.fps, self)
		self.updateWindow()

	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			removed_lines = self.inner_board.moveDown()
			self.external_board.score += removed_lines
			self.updateWindow()
		else:
			super(TetrisGame, self).timerEvent(event)

	def keyPressEvent(self, event):
		if not self.is_started or self.inner_board.current_tetris == tetrisShape().shape_empty:
			super(TetrisGame, self).keyPressEvent(event)
			return
		key = event.key()

		if key == Qt.Key_P:
			self.pause()
			return
		if self.is_paused:
			return

		elif key == Qt.Key_Left:
			self.inner_board.moveLeft()

		elif key == Qt.Key_Right:
			self.inner_board.moveRight()

		elif key == Qt.Key_Up:
			self.inner_board.rotateAnticlockwise()

		elif key == Qt.Key_Space:
			self.external_board.score += self.inner_board.dropDown()
		else:
			super(TetrisGame, self).keyPressEvent(event)
		self.updateWindow()



if __name__ == '__main__':
	app = QApplication([])
	tetris = TetrisGame()
	sys.exit(app.exec_())