import numpy as np

array = [1, 2, 3]

def readCoord():
    # readline_all.py
    f = open("C:\\Users\\MR Lab\\Documents\\drawing-doodle-bot\\output.txt", 'r')
    while True:
        line = f.readline()
        if(line == '\n'):
            print("z가 움직일 차례")
        else:
            # 라인 읽고 바로 x ,y move
            # line = line.split(' ')
            line = line.strip('\n')
            array = line.split()


            tmp_x = int(array[0])
            tmp_y = int(array[1])

            print(tmp_x)
            print(tmp_y)

            print("hi")



        if not line: break

    f.close()

readCoord()