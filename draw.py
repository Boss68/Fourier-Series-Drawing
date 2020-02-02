import pygame, numpy, math, time

pygame.init()
WINDOW=pygame.display.set_mode((800,600))
pygame.display.set_caption("Fourier Series Drawings")
size=200
drawingFont=pygame.font.SysFont('arial',size)
while drawingFont.size("False")[0]>100:
    size-=1
    drawingFont = pygame.font.SysFont('arial', size)
running=True
drawing=True
drawSurf=pygame.Surface((800,600))
drawSurf.fill((255,255,255))
lastPos=pygame.mouse.get_pos()
drawPath=[]
drawPathComplex=[]
drawPathX=[]
drawPathY=[]
curves=[]
curveLists=[]
curveListsReal=[]
curveListsImag=[]
pointres=500
startTime=time.time()
t=0
positions=[]
circles=200
timeScale=0.1
while running:
    if drawing==True:
        WINDOW.blit(drawSurf,(0,0))
        WINDOW.blit(drawingFont.render("Drawing", True, (0, 0, 0)), (0, 0))
        if not(pygame.Rect(700,0,100,50).collidepoint(*pygame.mouse.get_pos())):
            pygame.draw.rect(WINDOW,(128,128,128),pygame.Rect(700,0,100,50))
        else:
            if not(pygame.mouse.get_pressed()[0]):
                pygame.draw.rect(WINDOW, (64,64,64), pygame.Rect(700, 0, 100, 50))
            else:
                pygame.draw.rect(WINDOW, (32, 32, 32), pygame.Rect(700, 0, 100, 50))
        if not(pygame.Rect(0,550,50,50).collidepoint(*pygame.mouse.get_pos())):
            pygame.draw.rect(WINDOW,(128,128,128),pygame.Rect(0,550,50,50))
        else:
            if not(pygame.mouse.get_pressed()[0]):
                pygame.draw.rect(WINDOW, (64,64,64), pygame.Rect(0,550,50,50))
            else:
                pygame.draw.rect(WINDOW, (32, 32, 32), pygame.Rect(0,550,50,50))
        if pygame.mouse.get_pressed()[0]:
            if not(lastPos==pygame.mouse.get_pos()):
                #pygame.draw.circle(drawSurf,(0,0,0),pygame.mouse.get_pos(),3)
                #pygame.draw.circle(drawSurf, (0, 0, 0), lastPos, 3)
                pygame.draw.line(drawSurf,(0,0,0),pygame.mouse.get_pos(),lastPos)
                drawPath.append([pygame.mouse.get_pos(), lastPos])
                lastPos = pygame.mouse.get_pos()
        if len(drawPath) > 0:
            drawPathComplex = [(complex(*i[0]), -1) for i in drawPath]
            drawPathComplex.insert(0, (complex(*drawPath[0][1]), 0))
            period = 2
            inserts = []
            curves = []
            curveLists = []
            curves.append([0, 0, 0, False])
            for i in range(len(drawPath)):

                if i > 0 and drawPath[i][1] != drawPath[i - 1][0]:
                    curves[len(curves) - 1][1] = i + len(inserts)
                    curves.append([i + len(inserts), i + 1 + len(inserts),
                                   math.hypot(drawPath[i - 1][0][0] - drawPath[i][1][0],
                                              drawPath[i - 1][0][1] - drawPath[i][1][1]), True])
                    inserts.append(i)
                    curves.append([i + len(inserts), 0, 0, False])
                    curves[len(curves) - 1][2] += math.hypot(drawPath[i][0][0] - drawPath[i][1][0],
                                                             drawPath[i][0][1] - drawPath[i][1][1])
                    drawPathComplex[i] = (drawPathComplex[i][0], period * math.pi)
                    period += 4
                else:
                    curves[len(curves) - 1][2] += math.hypot(drawPath[i][0][0] - drawPath[i][1][0],
                                                             drawPath[i][0][1] - drawPath[i][1][1])
            curves[len(curves) - 1][1] = len(drawPathComplex) - 1 + len(inserts)
            remove = []
            for i in range(len(curves)):
                if curves[i][2] == 0:
                    remove.append(curves[i])
            for i in remove:
                curves.remove(i)
            period = 4
            for i in range(len(inserts)):
                drawPathComplex.insert(inserts[i] + 1 + i, (complex(*drawPath[inserts[i]][1]), period * math.pi))
                period += 4
            period -= 2
            drawPathComplex[len(drawPathComplex) - 1] = (drawPathComplex[len(drawPathComplex) - 1][0], period * math.pi)
            for i in curves:
                # print('Curve: '+str(i))
                # print('-----------')
                curveLists.append([])
                distance = 0
                for x in range(i[0], i[1] + 1):
                    if x > i[0]:
                        distance += math.hypot(*(drawPathComplex[x][0].real - drawPathComplex[x - 1][0].real,
                                                 drawPathComplex[x][0].imag - drawPathComplex[x - 1][0].imag))
                    if drawPathComplex[x][1] > 0:
                        curveLists[len(curveLists) - 1].append(drawPathComplex[x])
                    else:
                        drawPathComplex[x] = (
                        drawPathComplex[x][0], drawPathComplex[i[0]][1] + distance / i[2] * (2 * math.pi))
                        curveLists[len(curveLists) - 1].append(drawPathComplex[x])
            curveListsReal = []
            curveListsImag = []
            curveLists.append([curveLists[::-1][0][::-1][0],(curveLists[0][0][0],curveLists[::-1][0][::-1][0][1]+2*math.pi)])
            for q in range(len(curveLists)):
                curveListsReal.append([(x[0].real, x[1]) for x in curveLists[q]])
                curveListsImag.append([(x[0].imag, x[1]) for x in curveLists[q]])
            axes=[]
            for i in range(len(curveListsReal)):
                finalAxis = numpy.linspace(numpy.double(min([x[1] for x in curveListsReal[i]])),
                                           numpy.double(max([x[1] for x in curveListsReal[i]])), num=500, retstep=False)
                axes.append(finalAxis)
                interpCurvesReal = numpy.interp(finalAxis, [x[1] for x in curveListsReal[i]],
                                                [x[0] for x in curveListsReal[i]])
                interpCurvesImag = numpy.interp(finalAxis, [x[1] for x in curveListsImag[i]],
                                                [x[0] for x in curveListsImag[i]])
                curveListsReal[i] = interpCurvesReal
                curveListsImag[i] = interpCurvesImag
            # print(complex(*list(zip(curveListsReal[0],curveListsImag[0]))[::-1][0]), complex(*pygame.mouse.get_pos()))
            oneCurve=[]
            oneAxis=[]
            for i in range(len(curveListsReal)):
                for x in list(zip(curveListsReal[i],curveListsImag[i],axes[i])):
                    oneCurve.append(complex(*x[0:2]))
                    oneAxis.append(x[2])
            finalAxis=numpy.linspace(0,2*math.pi*len(curveLists),num=pointres*len(curveLists))
            finalCurve=[complex((x[0]-400)/300,-(x[1]-300)/300) for x in list(zip(numpy.interp(finalAxis,oneAxis,[i.real for i in oneCurve]),numpy.interp(finalAxis,oneAxis,[z.imag for z in oneCurve])))]
            finalAxis=[i/(2*math.pi*len(curveLists))*(2*math.pi) for i in finalAxis]
            #print(finalCurve)
            '''for i in range(len(finalCurve)):
                isReal=(((finalAxis[i]-2*math.pi)%(4*math.pi))-2*math.pi)>=0
                if isReal == 1:
                    pygame.draw.circle(WINDOW, (0, 0, 0), (int(finalCurve[i].real*300+400),int(-finalCurve[i].imag*300+300)), 3)
                elif isReal==0:
                    pygame.draw.circle(WINDOW, (255, 0, 0), (int(finalCurve[i].real*300+400),int(-finalCurve[i].imag*300+300)), 3)'''
    else:
        WINDOW.blit(drawingFont.render("Playing Back", True, (0, 0, 0)), (0, 0))
        t=time.time()-startTime
        interval=2*math.pi/len(curveLists)
        print("Circles: "+str(circles)+", Time Scale: "+str(timeScale))
        isReal = (((t * timeScale - interval) % (2 * interval)) - interval) >= 0
        #print(vec)
        lastVal=(400,300)
        val=0
        for i in range(len(vec)):
            #if int(abs(vec[i][1])*300)>0:
                #pygame.draw.circle(WINDOW,(0,0,0),(int(val.real*300+400),int(-val.imag*300+300)),int(abs(vec[i][1])*300),1)
            val+=vec[i][1]*(math.e**(complex(0,vec[i][0]*t*timeScale)))
            pygame.draw.line(WINDOW,(0,0,0),lastVal,(int(val.real*300+400),int(-val.imag*300+300)))
            lastVal=(int(val.real*300+400),int(-val.imag*300+300))
        positions.append([(int(val.real*300+400),int(-val.imag*300+300)),isReal])
        pygame.draw.circle(WINDOW,(255,0,0),(int(val.real*300+400),int(-val.imag*300+300)),3)
        if len(positions)>1:
            for i in range(len(positions)):
                if positions[i][1]:
                    if i>0:
                        pygame.draw.line(WINDOW,(0,0,0),positions[i][0],positions[i-1][0])
            #pygame.draw.lines(WINDOW,(0,0,0),False,positions)
        if not(pygame.Rect(700,0,100,50).collidepoint(*pygame.mouse.get_pos())):
            pygame.draw.rect(WINDOW,(128,128,128),pygame.Rect(700,0,100,50))
        else:
            if not(pygame.mouse.get_pressed()[0]):
                pygame.draw.rect(WINDOW, (64,64,64), pygame.Rect(700, 0, 100, 50))
            else:
                pygame.draw.rect(WINDOW, (32, 32, 32), pygame.Rect(700, 0, 100, 50))
    #print(drawPathComplex)
    #print('----------')
    #print(curveLists)
    #print(curveListsReal)
    #print(curveListsImag)
    #print('--done--')
    pygame.display.update()
    WINDOW.fill((255,255,255))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                timeScale+=0.01
                positions = []
                t = 0
            elif event.key==pygame.K_DOWN:
                timeScale-=0.01
                positions = []
                t = 0
        if event.type==pygame.MOUSEBUTTONDOWN:
            lastPos = pygame.mouse.get_pos()
            if event.button==1 and pygame.Rect(700,0,100,50).collidepoint(*pygame.mouse.get_pos()):
                if drawing==False:
                    drawing=True
                elif drawing==True and len(drawPath)>0:
                    startTime=time.time()
                    t=0
                    positions = []
                    vec = []

                    imagInt=2*math.pi/len(curveLists)
                    for i in range(circles):
                        vec.append((-round(circles / 2) + i, (1 / len(finalCurve)) * sum([finalCurve[x] * complex(
                            math.cos(-(-round(circles / 2) + i) * finalAxis[x]),
                            math.sin(-(-round(circles / 2) + i) * finalAxis[x])) for x in range(len(finalCurve))])))
                    formula=open('formula.txt','w')
                    formulaTxt='('
                    for i in vec:
                        formulaTxt+="%f\cdot cos(%f\cdot t)-%f\cdot sin(%f\cdot t)+"%(i[1].real,i[0],i[1].imag,i[0])
                    formulaTxt=formulaTxt[0:len(formulaTxt)-1]
                    formulaTxt+="\cdot (\\left(-1\\right) ^ {\\frac{\\left(\\frac{-\\left(\\operatorname{mod}\\left(t - %f, 2\cdot %f\\right)-%f\\right)}{\\operatorname{abs}\\left(\\operatorname{mod}\\left(t - %f, 2\cdot%f\\right)-%f\\right)}+1\\right)}{4}})"%(imagInt,imagInt,imagInt,imagInt,imagInt,imagInt)
                    formulaTxt+=','
                    for i in vec:
                        formulaTxt+="%f\cdot sin(%f\cdot t)+%f\cdot cos(%f\cdot t)+"%(i[1].real,i[0],i[1].imag,i[0])
                    formulaTxt = formulaTxt[0:len(formulaTxt) - 1]
                    formulaTxt += ')'
                    formula.write(formulaTxt)
                    formula.close()
                    print(formulaTxt)
                    drawing=False
            if len(drawPath)>0:
                if event.button==5:
                    circles+= 1
                    vec = []
                    for i in range(circles):
                        vec.append((-round(circles / 2) + i, (1 / len(finalCurve)) * sum([finalCurve[x] * complex(
                            math.cos(-(-round(circles / 2) + i) * finalAxis[x]),
                            math.sin(-(-round(circles / 2) + i) * finalAxis[x])) for x in range(len(finalCurve))])))
                    positions=[]
                    t=0
                    startTime = time.time()
                elif event.button==4:
                    if circles>1:
                        circles -= 1
                    vec = []
                    for i in range(circles):
                        vec.append((-round(circles / 2) + i, (1 / len(finalCurve)) * sum([finalCurve[x] * complex(
                            math.cos(-(-round(circles / 2) + i) * finalAxis[x]),
                            math.sin(-(-round(circles / 2) + i) * finalAxis[x])) for x in range(len(finalCurve))])))
                    positions=[]
                    t=0
                    startTime = time.time()
            #print(event.button)
            if event.button==1 and pygame.Rect(0,550,50,50).collidepoint(*pygame.mouse.get_pos()):
                drawSurf.fill((255,255,255))
                drawPath=[]
                drawPathComplex=[]