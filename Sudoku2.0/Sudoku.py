import multiprocessing
import random
import math
from multiprocessing import Pool


def get_random_unit():
    _num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(_num_list)
    return _num_list


def print_grid(arr, sds):
    for i in range(9):
        sds.append(arr[i])


def get_row(row, matrix):
    row_arr = []
    for v in matrix[row]:
        if v == 0:
            continue
        row_arr.append(v)
    return row_arr


def get_col(col, matrix):
    col_arr = []
    for i in range(9):
        val = matrix[i][col]
        if val == 0:
            continue
        col_arr.append(matrix[i][col])
    return col_arr


def get_block(num, matrix):
    col_arr = []
    seq = num % 3
    col_end = 9 if seq == 0 else seq * 3
    row_end = int(math.ceil(num / 3) * 3)
    for i in range(row_end - 3, row_end):
        for j in range(col_end - 3, col_end):
            val = matrix[i][j]
            if val != 0:
                col_arr.append(matrix[i][j])
    return col_arr


def get_block_seq(row, col):
    col_seq = int(math.ceil((col + 0.1) / 3))
    row_seq = int(math.ceil((row + 0.1) / 3))
    return 3 * (row_seq - 1) + col_seq


def get_enable_arr(row, col, matrix):
    avail_arr = get_random_unit()
    seq = get_block_seq(row, col)
    block = get_block(seq, matrix)
    row = get_row(row, matrix)
    col = get_col(col, matrix)
    unable_arr = list(set(block + row + col))
    for v in unable_arr:
        if v in avail_arr:
            avail_arr.remove(v)
    return avail_arr


def get1():
    matrix = []
    sds = []
    can_num = {}
    count = 0

    for i in range(9):
        matrix.append([0] * 9)

    num_list = get_random_unit()
    for row in range(3):
        for col in range(3):
            matrix[row][col] = num_list.pop(0)

    num_list = get_random_unit()
    for row in range(3, 6):
        for col in range(3, 6):
            matrix[row][col] = num_list.pop(0)

    num_list = get_random_unit()
    for row in range(6, 9):
        for col in range(6, 9):
            matrix[row][col] = num_list.pop(0)

    box_list = []
    for row in range(9):
        for col in range(9):
            if matrix[row][col] == 0:
                box_list.append({'row': row, 'col': col})

    i = 0
    while i < len(box_list):
        count += 1
        position = box_list[i]
        row = position['row']
        col = position['col']
        key = '%dx%d' % (row, col)
        if key in can_num:
            enable_arr = can_num[key]
        else:
            enable_arr = get_enable_arr(row, col, matrix)
            can_num[key] = enable_arr

        if len(enable_arr) <= 0:
            i -= 1
            if key in can_num:
                del (can_num[key])
            matrix[row][col] = 0
            continue
        else:
            matrix[row][col] = enable_arr.pop()
            i += 1

    print_grid(matrix, sds)
    return sds

# --------------------华丽の分割线--------------------

ac_num = 0
pausE = True
difficulty = 3

from tkinter import *
from tkinter import ttk
import time


# 写一个将难度数字化的字典
mode = {'简单': 1, '入门': 2, '困难': 3, '地狱': 4, '无解': 5}


def setDiff(difF):
    global difficulty
    global diff
    difF = mode.get(difF)
    try:
        difficulty = int(difF)
        diff.destroy()
    except:
        pass


diff = Tk()
diff.title('难度选择')
diff.geometry('300x90+600+300')
diff.resizable(0, 0)
Label(diff, text='选择你要挑战的难度!', font=('微软雅黑', 9)).pack()
cmb = ttk.Combobox(diff)
cmb.pack()
cmb['value'] = ('简单', '入门', '困难', '地狱', '无解')
Button(diff, text='我选好了', command=lambda: setDiff(cmb.get())).pack()


def generate(sds):
    global dwc
    global re
    global difficulty
    global steps
    global wrongs
    global rights
    global steP
    sol = Toplevel(root)
    sol.title('题解')
    Label(sol, text="题解",font=("Arial", 15)).place(x=170, y=40)
    sol.geometry('390x500+600+150')
    sol.resizable(0, 0)
    for i in range(0, 9):
        for j in range(0, 9):
            Label(sol, text=sds[i][j],font=("Arial", 15)).place(x=j * 30 + 67, y=i * 30 + 94)
    Button(sol, text="切回主页面",command=root.lift).place(x=250,y=430)
    window = Toplevel(root)
    Label(window, text="数独").pack()
    Button(window, text="切回主页面",
           command=root.lift).place(x=250,y=430)
    window.title('数独')
    window.geometry('390x500+600+150')
    window.resizable(0, 0)
    begin_time = 0
    dwc = difficulty * 9
    ac_name = None

    List = range(1, 82)
    try:
        ran = random.sample(List, dwc)
    except:
        if difficulty > 9:
            ran = random.sample(List, 9)
        elif difficulty < 0:
            ran = random.sample(List, 1)
        print('难度输入出现问题 你将无法通关')

    def setBlock(num, name):
        global begin_time
        begin_time = 0
        if begin_time == 0:
            begin_time = time.time()
        global ac_num
        global ac_name
        ac_name = None
        if ac_name != name and name != None and ac_name != None:
            ac_name.config(text='?', bg='orange', activebackground='orange', relief='groove')
        if name.cget('bg') != 'green':
            name.config(text='···', relief='sunken', bg='lightblue', activebackground='lightblue')
            ac_name = name
            ac_num = num
        else:
            ac_name = None

    def setNum(num):
        global ac_name
        global begin_time
        global dwc
        global ac_num
        global re
        global difficulty
        global steps
        global wrongs
        global rights
        global steP
        try:
            b_color = ac_name.cget('bg')
            if ac_num == num:
                ac_name.config(text='√', activebackground='green', relief='groove', bg='green')
            else:
                ac_name.config(text='×', activebackground='red', relief='groove')
            ac_name.flash()
            ac_name.flash()
            if ac_num == num:
                ac_name.config(text=str(num), activebackground='green', background='green', relief='groove')
            else:
                ac_name.config(text='?', bg='orange', activebackground='white', relief='groove')
            if ac_name.cget('bg') == 'green' and b_color == 'lightblue':
                dwc -= 1
                ac_name = None
                rights += 1
                steps += 1
            elif b_color == 'lightblue' and ac_name.cget('bg') == 'white':
                ac_name = None
                wrongs += 1
                steps += 1
            if dwc == 0:
                ac_name = None
                print('恭喜,你赢了!')
                Label(window, text='恭喜,你赢了!', font=('微软雅黑', 30), bg='lightgreen').place(x=52, y=50)
                use_time = round(time.time() - begin_time, 1)
                Label(window, text='用时' + str(use_time) + '秒  正确率' + str(round((rights / steps) * 100, 1)) + '%',
                      bg='yellow').place(x=113, y=121)
            ac_name = None

        except:
            pass

    def tipSs():
        '''global sds
        for ynfo in sds:
            print(ynfo)'''
        global ac_num
        global ac_name
        try:
            ac_name.config(text=str(ac_num))
            ac_name.flash()
            ac_name.config(text='···')
            setNum(ac_num)
        except:
            pass
    # 写一个求解数独的函数，用于一键求解
    def solve(sds):
        j = 0
        i = 0.7
        _count = 1
        for info in sds:
            for jnfo in info:
                j += 1
                for znfo in ran:
                    Label(window, text=jnfo, font=('微软雅黑', 10), relief='ridge', bg='grey').place(x=j * 36, y=i * 38,
                                                                                                     width=30,
                                                                                                     height=30)
            j = 0
            i += 1

    j = 0
    i = 0.7
    _count = 1
    wz = False
    def spaceBtn(i, j, ri, rj):
        name = 'a' + str(i + 1) + str(j + 1)
        name = Button(window, text='?', font=('微软雅黑', 10), relief='groove', bg='white', activebackground='white',
                      command=lambda: setBlock(sds[i][j], name))
        name.place(x=rj * 36, y=ri * 38, width=30, height=30)

    def numBtn(num):
        Button(window, text=str(num), font=('楷体', 15), relief='sunken', bg='white', activebackground='blue',
               command=lambda: setNum(num)).place(x=x * 42 + 9, y=380, width=37, height=37)
    for info in sds:
        for jnfo in info:
            j += 1
            for znfo in ran:
                if _count == znfo:
                    wz = True
            _count += 1
            if wz == True:
                spaceBtn(round(i - 1), j - 1, i, j)
                wz = False
            else:
                Label(window, text=jnfo, font=('微软雅黑', 10), relief='ridge', bg='grey').place(x=j * 36, y=i * 38,
                                                                                                 width=30, height=30)
        j = 0
        i += 1
    for x in range(0, 9):
        numBtn(x + 1)
    Button(window, text='提示', command=tipSs).place(x=50, y=430)
    Button(window,text='求解',command=lambda:solve(sds)).place(x=100,y=430)
    return window,sol


def producerPool():
    p = Pool(3)
    result_list = []
    sds = []
    try:
        for i in range(9):
            result_list.append(p.apply_async(get1))
    except:
            print('error')
    p.close()
    p.join()
    for result in result_list:
        sds.append(result)
    return sds


# 创建一个数独题解生成窗口的函数
def solver(sds):
    global sudoku
    sudoku = Tk()
    sudoku.geometry('1000x800+280+0')
    labels = []
    def display(sds,k):
        q = math.floor(k/3)
        z = k % 3
        Label(sudoku, text='题解' + str(k+1)).place(x=((12 * z) * 20) + 260,y=(12*q)*20+30)
        for i in range(0,9):
            for j in range(0,9):
                Label(sudoku,text=sds[i][j]).place(x=(j+12*z)*20+190,y=(i+12*q)*20+60)

    def back(window1,window2):
        window1.lift()
        window2.destroy()

    display(sds[0].get(),0)
    for i in range(0,9):
        display(sds[i].get(),i)
    Button(sudoku, text="切回主页面",
           command=lambda:back(root,sudoku)).place(x=770,y=730)
def main():

    diff.mainloop()
    sds = producerPool()
    windows = []
    sols = []
    global root
    root = Tk()
    Label(root, text="主页面").pack()
    for eg in sds:
        window,sol = generate(eg.get())
        windows.append(window)
        sols.append(sol)

    root.geometry("390x500+600+150")
    root.title("首页")
    # 设置按钮来选择数独
    Button(root, text="数独1", command=windows[0].lift,width=12, height=1).place(x=30,y=55)
    Button(root, text="题解1", command=sols[0].lift, width=12, height=1).place(x=30, y=90)
    Button(root, text="数独2", command=windows[1].lift,width=12, height=1).place(x=150,y=55)
    Button(root, text="题解2", command=sols[1].lift, width=12, height=1).place(x=150, y=90)
    Button(root, text="数独3", command=windows[2].lift,width=12, height=1).place(x=270,y=55)
    Button(root, text="题解3", command=sols[2].lift, width=12, height=1).place(x=270, y=90)
    Button(root, text="数独4", command=windows[3].lift,width=12, height=1).place(x=30,y=140)
    Button(root, text="题解4", command=sols[3].lift, width=12, height=1).place(x=30, y=175)
    Button(root, text="数独5", command=windows[4].lift,width=12, height=1).place(x=150,y=140)
    Button(root, text="题解5", command=sols[4].lift, width=12, height=1).place(x=150, y=175)
    Button(root, text="数独6", command=windows[5].lift,width=12, height=1).place(x=270,y=140)
    Button(root, text="题解6", command=sols[5].lift, width=12, height=1).place(x=270, y=175)
    Button(root, text="数独7", command=windows[6].lift,width=12, height=1).place(x=30,y=225)
    Button(root, text="题解7", command=sols[6].lift, width=12, height=1).place(x=30, y=260)
    Button(root, text="数独8", command=windows[7].lift,width=12, height=1).place(x=150,y=225)
    Button(root, text="题解8", command=sols[7].lift, width=12, height=1).place(x=150, y=260)
    Button(root, text="数独9", command=windows[8].lift,width=12, height=1).place(x=270,y=225)
    Button(root, text="题解9", command=sols[8].lift, width=12, height=1).place(x=270, y=260)
    Button(root,text="一键求解",command=lambda:solver(sds),width=12, height=3).place(x=150,y=330)
    root.mainloop()
    sudoku.mainloop()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()