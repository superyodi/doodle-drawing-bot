import math


dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)
moveX=0;moveY=0;moveZ=20;moveFlag=-1
pos = dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]


moveStroke = 2

dType.SetPTPCmd(api, 2, x, y, z + moveZ, rHead, 1)

f = open("C:\\Users\\MR Lab\\Documents\\drawing-doodle-bot\\output.txt", 'r')
while True:
    line = f.readline()

    if (line == '\n'):
        print("z가 움직일 차례")
        moveStroke = -1
        dType.SetPTPCmd(api, 2, x, y, z + moveZ, rHead, 1)
        moveStroke += 1
    else:
        # 라인 읽고 바로 x ,y move
        # line = line.split(' ')
        line = line.strip('\n')
        array = line.split()

        if not line: break

        tmpX = int(array[0])
        tmpY = int(array[1])

        dType.SetPTPCmd(api, 2, tmpX, tmpY, z, rHead, 1)
        print(moveStroke)
        moveStroke += 1


f.close()

