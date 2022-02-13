# 注：运行前需要用pip安装pygame与pygame_menu包
import pygame, time, pygame_menu, tkinter, tkinter.messagebox, os, importlib

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOARD_ORDER, BOARD_SIZE = 19, 30
BOARD_X0, BOARD_Y0 = 15, 15
GRID_NULL, GRID_BLACK, GRID_WHITE = 0, 1, 2
SPEED_X = [1, 0, 1, -1]
SPEED_Y = [0, 1, 1, 1]


def RT_is_five(grid, x, y, man):
    # print(x,y)
    for i in range(4):
        cnt = 0
        spd = [SPEED_X[i], SPEED_Y[i]]
        pos = [x - 4 * spd[0], y - 4 * spd[1]]
        # print('    ',spd)
        for j in range(9):
            try:
                player = grid[pos[1]][pos[0]]
            except:
                continue
            if player == man:
                cnt += 1
            else:
                cnt = 0
            # print('        ',pos[0],pos[1],cnt)
            pos[0] += spd[0]
            pos[1] += spd[1]
            if cnt >= 5:
                return True
    return False


def RT_draw_txt(scr, fnt, cls, txt, x, y):
    pic = fnt.render(txt, True, cls)
    scr.blit(pic, (x, y))
    return


def RT_get_flag_beads(grid, x, y, man, flag):
    beadsNum, powerNum = 1, 0
    for i in range(-1, -5, -1):
        tx, ty = x + i * SPEED_X[flag], y + i * SPEED_Y[flag]
        if tx < 0 or tx >= BOARD_ORDER or ty < 0 or ty >= BOARD_ORDER:
            break
        if grid[ty][tx] != man:
            powerNum += (grid[ty][tx] == GRID_NULL)
            break
        beadsNum = beadsNum + 1
    for i in range(1, 5, 1):
        tx, ty = x + i * SPEED_X[flag], y + i * SPEED_Y[flag]
        if tx < 0 or tx >= BOARD_ORDER or ty < 0 or ty >= BOARD_ORDER:
            break
        if grid[ty][tx] != man:
            powerNum += (grid[ty][tx] == GRID_NULL)
            break
        beadsNum = beadsNum + 1
    if beadsNum >= 5:
        beadsNum = 5
    return [beadsNum, powerNum]


ASSESS_WIN, ASSESS_ANS, ASSESS_COUNT = 2, 1, 0


def RT_get_assess_value(countList):
    assess, value = 0, 0
    if ([5, 2] in countList) or ([5, 1] in countList) or ([5, 0] in countList):
        assess, value = ASSESS_WIN, 200
    elif [4, 2] in countList:
        assess, value = ASSESS_ANS, 100
    else:
        value += countList.count([4, 1]) * 70
        value += countList.count([3, 2]) * 60
        value += countList.count([3, 1]) * 30
        value += countList.count([2, 2]) * 20
        value += countList.count([2, 1]) * 15
        assess = ASSESS_COUNT
    return assess, value


class CLS_assess(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.bAssess, self.wAssess = 0, 0
        self.bValue, self.wValue = 0, 0
        self.bCount = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.wCount = [[0, 0], [0, 0], [0, 0], [0, 0]]
        return

    def beads(self, grid):
        for flag in (0, 1, 2, 3):
            self.bCount[flag] = RT_get_flag_beads(grid, self.x, self.y, GRID_BLACK, flag)
            self.wCount[flag] = RT_get_flag_beads(grid, self.x, self.y, GRID_WHITE, flag)
        return

    def assess(self, grid):
        self.beads(grid)
        self.bAssess, self.bValue = RT_get_assess_value(self.bCount)
        self.wAssess, self.wValue = RT_get_assess_value(self.wCount)
        return


class CLS_gobang(object):
    def draw_board(self):
        self.board.fill((240, 200, 0))
        L = BOARD_X0 + (BOARD_ORDER - 1) * BOARD_SIZE
        for i in range(BOARD_X0, SCREEN_HEIGHT, BOARD_SIZE):
            pygame.draw.line(self.board, (0, 0, 0), (BOARD_X0, i), (L, i), 1)
            pygame.draw.line(self.board, (0, 0, 0), (i, BOARD_Y0), (i, L), 1)
        for i in range(1, 20):
            RT_draw_txt(self.board, self.fontScore, (0, 0, 0), str(i), BOARD_X0 + (i - 1) * BOARD_SIZE - 4, BOARD_Y0 - 12)
            RT_draw_txt(self.board, self.fontScore, (0, 0, 0), str(i), BOARD_X0 - 6 - len(str(i)) * 4, BOARD_Y0 + (i - 1) * BOARD_SIZE - 4)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 3 * BOARD_SIZE, BOARD_Y0 + 3 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 9 * BOARD_SIZE, BOARD_Y0 + 3 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 15 * BOARD_SIZE, BOARD_Y0 + 3 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 3 * BOARD_SIZE, BOARD_Y0 + 9 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 9 * BOARD_SIZE, BOARD_Y0 + 9 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 15 * BOARD_SIZE, BOARD_Y0 + 9 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 3 * BOARD_SIZE, BOARD_Y0 + 15 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 9 * BOARD_SIZE, BOARD_Y0 + 15 * BOARD_SIZE), 6)
        pygame.draw.circle(self.board, (0, 0, 0), (BOARD_X0 + 15 * BOARD_SIZE, BOARD_Y0 + 15 * BOARD_SIZE), 6)
        pygame.draw.rect(self.board, (0, 0, 0), (BOARD_X0 - 1, BOARD_Y0 - 1, L + 3 - BOARD_X0, L + 3 - BOARD_Y0), 1)
        return

    def draw_menu(self):
        pass

    def __init__(self, bPic, wPic, x0, y0):
        self.serialFlag = True
        self.serial_grid = []
        self.bMan, self.wMan = bPic, wPic
        self.font = pygame.font.Font(None, 32)
        self.fontScore = pygame.font.Font(None, 16)
        self.fontWin = pygame.font.Font(None, 96)
        self.board = pygame.Surface((570, 570))
        self.draw_board()
        self.x0, self.y0 = x0, y0
        self.grid_init()
        self.sysStat = -1
        self.assessFlag = False
        self.winner = -1
        self.count = 0
        self.chess_list = []
        return

    def grid_init(self):
        self.grid = []
        for y in range(BOARD_ORDER):
            line = [GRID_NULL] * BOARD_ORDER
            self.grid.append(line)
        for y in range(BOARD_ORDER):
            line = [-1] * BOARD_ORDER
            self.serial_grid.append(line)
        self.assessList = []
        for y in range(BOARD_ORDER):
            line = []
            for x in range(BOARD_ORDER):
                score = CLS_assess(x, y)
                line.append(score)
            self.assessList.append(line)
        self.bMaxAssess, self.bMaxValue, self.bpX, self.bpY = 0, 0, 9, 9
        self.wMaxAssess, self.wMaxValue, self.wpX, self.wpY = 0, 0, -1, -1
        self.SumValue, self.pX, self.pY = 0, -1, -1
        # self.grid[9][9] = GRID_BLACK
        # self.serial_grid[9][9] = 1
        return

    def draw_chess(self, scr):
        mL = []
        for y in range(BOARD_ORDER):
            line = self.serial_grid[y]
            mL.append(max(line))
        m = str(max(mL))
        for y in range(BOARD_ORDER):
            for x in range(BOARD_ORDER):
                player = self.grid[y][x]
                if (player == GRID_BLACK and ai_first == True) or (player == GRID_WHITE and ai_first == False):
                    scr.blit(self.bMan, (self.x0 + x * BOARD_SIZE, self.y0 + y * BOARD_SIZE))
                elif (player == GRID_WHITE and ai_first == True) or (player == GRID_BLACK and ai_first == False):
                    scr.blit(self.wMan, (self.x0 + x * BOARD_SIZE, self.y0 + y * BOARD_SIZE))
                if self.assessFlag == True:
                    pnt = self.assessList[y][x]
                    if pnt.bAssess > 0 or pnt.bValue > 0:
                        txt = str(pnt.bAssess) + ',' + str(pnt.bValue)
                        RT_draw_txt(scr, self.fontScore, (0, 0, 0), txt, self.x0 + x * BOARD_SIZE, self.y0 + y * BOARD_SIZE + 2)
                    if pnt.wAssess > 0 or pnt.wValue > 0:
                        txt = str(pnt.wAssess) + ',' + str(pnt.wValue)
                        RT_draw_txt(scr, self.fontScore, (255, 255, 255), txt, self.x0 + x * BOARD_SIZE, self.y0 + y * BOARD_SIZE + 16)
                if self.serialFlag == True and player != GRID_NULL:
                    serial = str(abs(self.serial_grid[y][x]))
                    color = None
                    if (player == GRID_BLACK and ai_first == True) or (player == GRID_WHITE and ai_first == False):
                        color = (255, 255, 255)
                    elif (player == GRID_WHITE and ai_first == True) or (player == GRID_BLACK and ai_first == False):
                        color = (0, 0, 0)
                    RT_draw_txt(scr, self.fontScore, color, serial, self.x0 + (x + 0.5) * BOARD_SIZE - len(serial) * 4, self.y0 + y * BOARD_SIZE + 9)
                    if serial == m:
                        pygame.draw.rect(scr, (255, 0, 0), (self.x0 + x * BOARD_SIZE, self.y0 + y * BOARD_SIZE, BOARD_SIZE, BOARD_SIZE), 4)
        return

    def draw(self, scr, events):
        global timer
        if self.sysStat >= 0:
            scr.fill((180, 140, 0))
            scr.blit(self.board, (self.x0, self.y0))
            self.draw_chess(scr)
            if self.sysStat == 1:
                txt, cls = white_name + ' WIN!!', (0, 255, 0)
                if self.winner == GRID_BLACK:
                    txt, cls = black_name + ' WIN', (255, 0, 0)
                elif self.winner == GRID_NULL:
                    txt, cls = 'TIE!!', (0, 0, 255)
                RT_draw_txt(scr, self.fontWin, cls, txt, 200, 290)
            info_menu.update(events)
            t = time.time()
            inter = t - t0
            m = inter // 60
            s = inter // 1 % 60
            timer.set_title(str('%02d' % int(m)) + ':' + str('%02d' % int(s)))
            info_menu.draw(screen)
            for i in range(30):
                pygame.draw.line(screen, (0, 0, 0), (600, i * 20), (600, i * 20 + 15), 2)
        elif self.sysStat == -1:
            setting_menu.update(events)
            setting_menu.draw(screen)
        return

    def grid_assess(self):
        self.bMaxAssess, self.bMaxValue, self.bpX, self.bpY = 0, 0, -1, -1
        self.wMaxAssess, self.wMaxValue, self.wpX, self.wpY = 0, 0, -1, -1
        self.SumValue, self.pX, self.pY = 0, -1, -1
        for y in range(BOARD_ORDER):
            for x in range(BOARD_ORDER):
                if self.grid[y][x] != GRID_NULL:
                    continue
                self.assessList[y][x].assess(self.grid)
                pnt = self.assessList[y][x]
                if (pnt.bAssess > self.bMaxAssess) or ((pnt.bAssess == self.bMaxAssess) and (pnt.bValue > self.bMaxValue)):
                    self.bMaxAssess, self.bMaxValue = pnt.bAssess, pnt.bValue
                    self.bpX, self.bpY = x, y
                if (pnt.wAssess > self.wMaxAssess) or ((pnt.wAssess == self.wMaxAssess) and (pnt.wValue > self.wMaxValue)):
                    self.wMaxAssess, self.wMaxValue = pnt.wAssess, pnt.wValue
                    self.wpX, self.wpY = x, y
                if pnt.wValue + pnt.bValue > self.SumValue:
                    self.SumValue = pnt.wValue + pnt.bValue
                    self.pX, self.pY = x, y
        return

    def grid_policy(self):
        if self.bMaxAssess == ASSESS_WIN:
            # print('ASSESS_WIN:', self.bpX, self.bpY)
            return self.bpX, self.bpY
        elif self.wMaxAssess == ASSESS_WIN:
            # print('ASSESS_WIN:', self.wpX, self.wpY)
            return self.wpX, self.wpY
        elif self.bMaxAssess > ASSESS_COUNT:
            # print('B ASSESS_COUNT:', self.bpX, self.bpY)
            return self.bpX, self.bpY
        elif self.wMaxAssess > ASSESS_COUNT:
            # print('W ASSESS_COUNT:', self.wpX, self.wpY)
            return self.wpX, self.wpY
        else:
            # print('SUM ASSESS_COUNT:', self.pX, self.pY)
            return self.pX, self.pY

    def eventkey(self, key):
        if self.sysStat == -1:
            return
        if key == pygame.K_RETURN:
            restart(None, None)
        if key == pygame.K_ESCAPE:
            escape(None, None)
        if key == pygame.K_n:
            self.serialFlag = not self.serialFlag
            seri.set_value(self.serialFlag)
        return

    def do_next(self):
        if self.sysStat != 0:
            return
        self.count += 1
        x, y = white_program.gobang.do_chess(self.grid)
        if x == -1 and y == -1:
            self.sysStat = 1
            self.winner = GRID_NULL
            return
        self.grid[y][x] = GRID_WHITE
        self.serial_grid[y][x] = self.count
        self.count += 1
        x, y = black_program.gobang.do_chess(self.grid)
        self.grid[y][x] = GRID_BLACK
        self.serial_grid[y][x] = self.count
        print(x, y)


def enter_game(*args, **kwargs):
    global GRID_WHITE, GRID_BLACK
    if black_file == '' or white_file == '':
        tkinter.messagebox.showerror('警告', '请选择黑子和白子的程序')
        return
    gobang.sysStat = 0
    gobang.grid[9][9] = GRID_BLACK
    gobang.count = 1
    global black_program, white_program
    black_program = importlib.import_module(black_file[:-3])
    white_program = importlib.import_module(white_file[:-3])
    white_program.change_color()


def change_black_file(*args, **kwargs):
    global black_file
    black_file = args[0][0][0]


def change_white_file(*args, **kwargs):
    global white_file
    white_file = args[0][0][0]


def change_black_name(*args, **kwargs):
    global black_name, player
    black_name = args[0]
    player.set_title(user_name)
    print(user_name)


def change_white_name(*args, **kwargs):
    global white_name, ai
    white_name = args[0]
    ai.set_title(user_name)


def change_n(*args, **kwargs):
    gobang.serialFlag = args[0]


def escape(*args, **kwargs):
    stat = tkinter.messagebox.askokcancel('退出？', '即将退出对局，进度将被清空')
    if stat:
        gobang.__init__(bPic, wPic, 20, 20)


def restart(*args, **kwargs):
    stat = tkinter.messagebox.askokcancel('重开？', '即将清空棋盘')
    if stat:
        gobang.__init__(bPic, wPic, 20, 20)
        enter_game(args, kwargs)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Realthink AI Gobang Terminator')
ai_first = True
black_name = 'black'
white_name = 'white'
black_file = ''
white_file = ''
# ----------pic defiition----------
iPic = pygame.image.load('ico.bmp')
iPic.set_colorkey((255, 255, 255))
pygame.display.set_icon(iPic)
wPic = pygame.image.load('WCMan.bmp')
wPic.set_colorkey((255, 0, 0))
pygame.image.save(wPic, 'white_chess.bmp')
bPic = pygame.image.load('BCMan.bmp')
bPic.set_colorkey((255, 0, 0))
pygame.image.save(bPic, 'black_chess.bmp')
# ----------framework----------
gobang = CLS_gobang(bPic, wPic, 20, 20)
# ----------menu definition-----------
theme = pygame_menu.themes.THEME_ORANGE.copy()
theme.title = False
theme.title_font = 'simkai.ttf'
theme.widget_font = 'simkai.ttf'
theme.title_font_size = 30
theme.widget_font_size = 20
theme.widget_font_color = (3,76,100)
theme.background_color = (220,182,107)
theme.title_background_color = (238,188,89)
theme.title_font_color = (175,208,151)
theme.selection_color = (43,153,204)
setting_menu = pygame_menu.menu.Menu('设置', 800, 600, theme=theme)
fList = os.listdir()
fileList = []
count = 0
for i in range(len(fList)):
    if fList[i][-3:] == '.py':
        fileList.append((fList[i], count))
        count += 1
print(fileList)
selc1 = setting_menu.add.dropselect('黑子程序', fileList)
selc1.set_onchange(change_black_file)
name1 = setting_menu.add.text_input('黑子昵称：', default='black')
name1.set_onchange(change_black_name)
selc2 = setting_menu.add.dropselect('白子程序', fileList)
selc2.set_onchange(change_white_file)
name2 = setting_menu.add.text_input('白子昵称：', default='white')
name2.set_onchange(change_white_name)
ensure = setting_menu.add.button('开始模拟')
ensure.set_onreturn(enter_game)
info_menu = pygame_menu.menu.Menu('菜单', 200, 600, center_content=False, position=(600, 0, False), theme=theme)
inter0 = info_menu.add.vertical_margin(15)
timer = info_menu.add.label('0:0')
t0 = time.time()
inter1 = info_menu.add.vertical_margin(30)
black_pic = pygame_menu.baseimage.BaseImage('black_chess.bmp')
white_pic = pygame_menu.baseimage.BaseImage('white_chess.bmp')
bc = info_menu.add.image(black_pic)
player = info_menu.add.label('black')
vs = info_menu.add.image('vs.bmp', scale=(0.1, 0.1))
ai = info_menu.add.label('white')
wc = info_menu.add.image(white_pic)
inter2 = info_menu.add.vertical_margin(30)
seri = info_menu.add.toggle_switch('序号标记', default=True, state_text=('关', '开'),
                                   state_text_font='simkai.ttf', state_text_font_size=18,
                                   state_color=((238,188,89), (175,209,151)), width=75)
seri.set_onchange(change_n)
inter3 = info_menu.add.vertical_margin(30)
clr = info_menu.add.button('清屏')
clr.set_onreturn(restart)
esc = info_menu.add.button('退出')
esc.set_onreturn(escape)
# ----------main loop----------
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            gobang.eventkey(event.key)
    gobang.do_next()
    gobang.draw(screen, events)
    pygame.display.update()
