import pygame, math, time, numpy, os

WINDOWdimensions=(800,600)
pygame.init()
def loadImg(imgName):
    e=math.e
    k=2
    sigma=1.4
    deviationkernel=[[] for i in range(2*k+1)]
    for i in range(2*k+1):
        for j in range(2*k+1):
            deviationkernel[j].append((1/(2*math.pi*(sigma**2)))*(e**(-((((i+1)-(k+1))**2+((j+1)-(k+1))**2)/(2*sigma**2)))))
    for i in deviationkernel:
        print(i)
    testimg=pygame.image.load(imgName)
    pygame.image.save(testimg,"currentImage.png")
    smallerDim=testimg.get_size().index(min(testimg.get_size()))
    dimensions=(int(WINDOWdimensions[1] * testimg.get_size()[0] / testimg.get_size()[1]),WINDOWdimensions[1])
    if dimensions[0]>WINDOWdimensions[0] or dimensions[1]>WINDOWdimensions[1]:
        dimensions=(WINDOWdimensions[0],int(WINDOWdimensions[0]*testimg.get_size()[1]/testimg.get_size()[0]))
    testimg=pygame.transform.scale(testimg, dimensions)
    print(testimg.get_size())
    for x in range(testimg.get_width()):
        for y in range(testimg.get_height()):
            testimg.set_at((x,y),[sum(list(testimg.get_at((x,y)))[0:3])/3 for i in range(3)])
    #WINDOW=pygame.display.set_mode((testimg.get_size()[0]*2,testimg.get_size()[1]))
    #pygame.display.set_caption('Gaussian Blur')
    gaussianboi=pygame.Surface(testimg.get_size())
    running=True
    deviationsum=sum([sum(i) for i in deviationkernel])
    #print(deviationsum)
    avgr=0
    avgg=0
    avgb=0
    for x in range(gaussianboi.get_width()):
        for y in range(gaussianboi.get_height()):
            avgr=0
            avgg=0
            avgb=0
            for i in range(len(deviationkernel)):
                for j in range(len(deviationkernel)):
                    if x+i-k>=0 and x+i-k<gaussianboi.get_width() and y+j-k>=0 and y+j-k<gaussianboi.get_height():
                        avgr+=testimg.get_at((x+i-k,y+j-k))[0]*deviationkernel[j][i]
                        avgg+=testimg.get_at((x+i-k,y+j-k))[1]*deviationkernel[j][i]
                        avgb+=testimg.get_at((x+i-k,y+j-k))[2]*deviationkernel[j][i]
            avgr/=deviationsum
            avgg/=deviationsum
            avgb/=deviationsum
            gaussianboi.set_at((x,y),(avgr,avgg,avgb))
    k=1
    img=gaussianboi
    gxkernel=[[-1,0,1],[-2,0,2],[-1,0,1]]
    gykernel=[[-1,-2,-1],[0,0,0],[1,2,1]]
    pixelrounddirs={}
    #WINDOW=pygame.display.set_mode((img.get_width()*2,img.get_height()))
    #pygame.display.set_caption('Calculate Derivatives')
    gx=0
    gy=0
    gxsum=sum([sum(i) for i in gxkernel])
    gysum=sum([sum(i) for i in gykernel])
    normalizemag=pygame.Surface(img.get_size())
    magnitudes=[[] for i in range(img.get_height())]
    newmags=[]
    suppression=pygame.Surface((img.get_size()))
    allvals=[[] for i in range(img.get_height())]
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            gx=0
            gy=0
            for i in range(len(gxkernel)):
                for j in range(len(gxkernel)):
                    if x + i - k >= 0 and x + i - k < img.get_width() and y + j - k >= 0 and y + j - k < img.get_height():
                        gx+=img.get_at((x+i-k,y+j-k))[0]*gxkernel[j][i]
                        gy += img.get_at((x + i - k, y + j - k))[0] * gykernel[j][i]
            magnitudes[y].append(math.sqrt(gx**2+gy**2))
            if (math.atan2(-gy,gx)/math.pi*180<=112.5 and math.atan2(-gy,gx)/math.pi*180>=67.5) or (math.atan2(-gy,gx)/math.pi*180>=-112.5 and math.atan2(-gy,gx)/math.pi*180<=-67.5):
                pixelrounddirs[(x,y)]=90
            elif (math.atan2(-gy,gx)/math.pi*180<=157.5 and math.atan2(-gy,gx)/math.pi*180>=112.5) or (math.atan2(-gy,gx)/math.pi*180<=-22.5 and math.atan2(-gy,gx)/math.pi*180>=-67.5):
                pixelrounddirs[(x,y)]=135
            elif (math.atan2(-gy,gx)/math.pi*180<=180 and math.atan2(-gy,gx)/math.pi*180>=157.5) or (math.atan2(-gy,gx)/math.pi*180<=22.5 and math.atan2(-gy,gx)/math.pi*180>=0) or (math.atan2(-gy,gx)/math.pi*180<=0 and math.atan2(-gy,gx)/math.pi*180>=-22.5) or (math.atan2(-gy,gx)/math.pi*180<=-157.5 and math.atan2(-gy,gx)/math.pi*180>=-180):
                pixelrounddirs[(x,y)]=0
            elif (math.atan2(-gy,gx)/math.pi*180<=67.5 and math.atan2(-gy,gx)/math.pi*180>=22.5) or (math.atan2(-gy,gx)/math.pi*180<=-112.5 and math.atan2(-gy,gx)/math.pi*180>=-157.5):
                pixelrounddirs[(x,y)]=45
            print('x=%s,y=%s,gx=%s, gy=%s,g=%s,o=%s'%(x,y,gx,gy,math.sqrt(gx**2+gy**2),math.atan2(-gy,gx)/math.pi*180))
    for i in magnitudes:
        for x in i:
            newmags.append(x)
    biggest=max(newmags)
    lowest=min(newmags)
    color=0
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color=[round(255*((magnitudes[y][x]-lowest)/(biggest-lowest))) for i in range(3)]
            normalizemag.set_at((x,y),color)
    running=True
    currentedgedir=0
    suppress=True
    pixelsremaining={}
    print('suppression time!')
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            print(x,y,img.get_size())
            if x > 0 and x < img.get_width() - 1 and y>0 and y<img.get_height()-1:
                suppress=True
                currentedgedir=pixelrounddirs[(x,y)]
                if currentedgedir==0:
                    if magnitudes[y][x]>magnitudes[y][x+1] and magnitudes[y][x]>magnitudes[y][x-1]:
                        suppress=False
                elif currentedgedir==45:
                    if magnitudes[y][x]>magnitudes[y-1][x+1] and magnitudes[y][x]>magnitudes[y+1][x-1]:
                        suppress=False
                elif currentedgedir==90:
                    if magnitudes[y][x]>magnitudes[y+1][x] and magnitudes[y][x]>magnitudes[y-1][x]:
                        suppress=False
                elif currentedgedir==135:
                    if magnitudes[y][x]>magnitudes[y+1][x+1] and magnitudes[y][x]>magnitudes[y-1][x-1]:
                        suppress=False
                if suppress==True:
                    suppression.set_at((x,y),(0,0,0))
                else:
                    pixelsremaining[(x,y)]=(magnitudes[y][x],currentedgedir)
                    color = [round(255 * ((magnitudes[y][x] - lowest) / (biggest - lowest))) for i in range(3)]
                    suppression.set_at((x,y),color)
    #doublethresh
    highthresh=biggest*0.07
    lowthresh=highthresh*0.05
    weak=25
    strong=255
    doublethresh=pygame.Surface(img.get_size())
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            try:
                if pixelsremaining[(x,y)][0]>=highthresh:
                    doublethresh.set_at((x,y),(strong,strong,strong))
                elif pixelsremaining[(x,y)][0]<highthresh and pixelsremaining[(x,y)][0]>=lowthresh:
                    doublethresh.set_at((x,y),(weak,weak,weak))
                elif pixelsremaining[(x,y)][0]<lowthresh:
                    doublethresh.set_at((x,y),(0,0,0))
            except Exception:
                None
    #hysteresis
    hysteresis=doublethresh
    dirs={0:(1,0),1:(1,1),2:(0,1),3:(-1,1),4:(-1,0),5:(-1,-1),6:(0,-1),7:(1,-1)}
    lasthysteresis=pygame.Surface(img.get_size())
    while lasthysteresis!=hysteresis:
        lasthysteresis=hysteresis
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                if hysteresis.get_at((x,y))==(weak,weak,weak):
                    if x>0 and x<img.get_width()-1 and y>0 and y<img.get_height()-1:
                        for i in range(8):
                            if hysteresis.get_at((x+dirs[i][0],y+dirs[i][1]))==(strong,strong,strong):
                                hysteresis.set_at((x,y),(strong,strong,strong))
                                break
                        else:
                            hysteresis.set_at((x, y), (0,0,0))
    points=[]
    getcurve=hysteresis
    extremey=[getcurve.get_height(),0]
    extremex=[getcurve.get_width(),0]
    for x in range(getcurve.get_width()):
        for y in range(getcurve.get_height()):
            if (getcurve.get_at((x, y))[0] + getcurve.get_at((x, y))[1] + getcurve.get_at((x, y))[2]) / 3 > 128:
                getcurve.set_at((x, y), (255, 255, 255))
            else:
                getcurve.set_at((x, y), (0, 0, 0))
    for i in range(getcurve.get_height()):
        for x in range(getcurve.get_width()):
            if getcurve.get_at((x, i)) == (255, 255, 255):
                if x < extremex[0]:
                    extremex[0] = x
                if x > extremex[1]:
                    extremex[1] = x
                if i < extremey[0]:
                    extremey[0] = i
                if i > extremey[1]:
                    extremey[1] = i
    boundedcurves = pygame.Surface((abs(extremex[0] - extremex[1]) + 1, abs(extremey[0] - extremey[1]) + 1))
    boundedcurves.blit(getcurve, (0, 0), pygame.Rect(extremex[0], extremey[0], abs(extremex[0] - extremex[1]) + 1,
                                                     abs(extremey[0] - extremey[1]) + 1))
    dirs = {0: (0, 1), 1: (-1, 1), 2: (-1, 0), 3: (-1, -1), 4: (0, -1), 5: (1, -1), 6: (1, 0), 7: (1, 1)}
    for x in range(boundedcurves.get_width()):
        for y in range(boundedcurves.get_height()):
            if boundedcurves.get_at((x, y)) == (255, 255, 255):
                points.append((x, y))
    path = []
    availablePoints = points[::]
    currentPoint = points[0]
    while availablePoints != []:
        availablePoints.remove(currentPoint)
        nearby = [(currentPoint[0] + dirs[i][0], currentPoint[1] + dirs[i][1]) for i in range(8)]
        if len(availablePoints) > 0:
            closestPoint = availablePoints[
                [math.hypot(currentPoint[0] - x[0], currentPoint[1] - x[1]) for x in availablePoints].index(
                    min([math.hypot(currentPoint[0] - x[0], currentPoint[1] - x[1]) for x in availablePoints]))]
        if closestPoint in nearby:
            path.append([closestPoint, currentPoint])
        currentPoint = closestPoint[::]
    drawPath = path[::]
    for i in drawPath:
        pygame.draw.line(drawSurf, (0, 0, 0), i[0], i[1])
    return drawPath
WINDOW=pygame.display.set_mode((WINDOWdimensions[0],WINDOWdimensions[1]))
pygame.display.set_caption("Fourier Series Drawings")
size=200
drawingFont=pygame.font.SysFont('arial',size)
while drawingFont.size("False")[0]>WINDOWdimensions[0]/8:
    size-=1
    drawingFont = pygame.font.SysFont('arial', size)
running=True
drawing=True
drawSurf=pygame.Surface((WINDOWdimensions[0],WINDOWdimensions[1]))
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
circles=310
drawCircles=1
timeScale=0.5
availExt=['.jpg','.jpeg','.png','.gif','.bmp','.pcx','.tga','.tif','.lbm','.pbm','.pgm','.ppm','.xpm']
gui=True
while running:
    if drawing==True:
        WINDOW.blit(drawSurf,(0,0))
        if gui:
            WINDOW.blit(drawingFont.render("Drawing", True, (0, 0, 0)), (0, 0))
            if not(pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12).collidepoint(*pygame.mouse.get_pos())):
                pygame.draw.rect(WINDOW,(128,128,128),pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12))
            else:
                if not(pygame.mouse.get_pressed()[0]):
                    pygame.draw.rect(WINDOW, (64,64,64), pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12))
                else:
                    pygame.draw.rect(WINDOW, (32, 32, 32), pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12))
            if not(pygame.Rect(0,WINDOWdimensions[1]*11/12,WINDOWdimensions[1]/12,WINDOWdimensions[1]/12).collidepoint(*pygame.mouse.get_pos())):
                pygame.draw.rect(WINDOW,(128,128,128),pygame.Rect(0,WINDOWdimensions[1]*11/12,WINDOWdimensions[1]/12,WINDOWdimensions[1]/12))
            else:
                if not(pygame.mouse.get_pressed()[0]):
                    pygame.draw.rect(WINDOW, (64,64,64), pygame.Rect(0,WINDOWdimensions[1]*11/12,WINDOWdimensions[1]/12,WINDOWdimensions[1]/12))
                else:
                    pygame.draw.rect(WINDOW, (32, 32, 32), pygame.Rect(0,WINDOWdimensions[1]*11/12,WINDOWdimensions[1]/12,WINDOWdimensions[1]/12))
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
            if len(curveLists)%2==0:
                curveLists=curveLists[0:len(curveLists)-1]
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
            finalCurve=[complex((x[0]-(WINDOWdimensions[0]/2))/(WINDOWdimensions[1]/2),-(x[1]-(WINDOWdimensions[1]/2))/(WINDOWdimensions[1]/2)) for x in list(zip(numpy.interp(finalAxis,oneAxis,[i.real for i in oneCurve]),numpy.interp(finalAxis,oneAxis,[z.imag for z in oneCurve])))]
            finalAxis=[i/(2*math.pi*len(curveLists))*(2*math.pi) for i in finalAxis]
            #print(finalCurve)
            '''for i in range(len(finalCurve)):
                isReal=(((finalAxis[i]-2*math.pi)%(4*math.pi))-2*math.pi)>=0
                if isReal == 1:
                    pygame.draw.circle(WINDOW, (0, 0, 0), (int(finalCurve[i].real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-finalCurve[i].imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2))), 3)
                elif isReal==0:
                    pygame.draw.circle(WINDOW, (255, 0, 0), (int(finalCurve[i].real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-finalCurve[i].imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2))), 3)'''
    else:
        if gui:
            WINDOW.blit(drawingFont.render("Playing Back", True, (0, 0, 0)), (0, 0))
        t=(time.time()-startTime)%(2*math.pi/timeScale)
        interval=2*math.pi/len(curveLists)
        isReal = (((t * timeScale - interval) % (2 * interval)) - interval) >= 0
        print("Circles: "+str(circles)+", Time Scale: "+str(timeScale))
        #print(vec)
        lastVal=((WINDOWdimensions[0]/2),(WINDOWdimensions[1]/2))
        val=0
        for i in range(len(vec)):
            #if int(abs(vec[i][1])*(WINDOWdimensions[1]/2))>0:
                #pygame.draw.circle(WINDOW,(0,0,0),(int(val.real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-val.imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2))),int(abs(vec[i][1])*(WINDOWdimensions[1]/2)),1)
            val+=vec[i][1]*(math.e**(complex(0,vec[i][0]*t*timeScale)))
            if drawCircles>1:
                pygame.draw.circle(WINDOW,(0,0,0),lastVal,abs(vec[i][1])*(WINDOWdimensions[1]/2),1)
            if drawCircles>0:
                pygame.draw.line(WINDOW,(0,0,0),lastVal,(int(val.real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-val.imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2))))
            lastVal=(int(val.real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-val.imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2)))
        positions.append([(int(val.real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-val.imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2))),isReal])
        if drawCircles>0:
            pygame.draw.circle(WINDOW,(255,0,0),(int(val.real*(WINDOWdimensions[1]/2)+(WINDOWdimensions[0]/2)),int(-val.imag*(WINDOWdimensions[1]/2)+(WINDOWdimensions[1]/2))),3)
        if len(positions)>1:
            for i in range(len(positions)):
                if positions[i][1]:
                    if i>0:
                        pygame.draw.line(WINDOW,(0,0,0),positions[i][0],positions[i-1][0])
            #pygame.draw.lines(WINDOW,(0,0,0),False,positions)
        if gui:
            if not(pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12).collidepoint(*pygame.mouse.get_pos())):
                pygame.draw.rect(WINDOW,(128,128,128),pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12))
            else:
                if not(pygame.mouse.get_pressed()[0]):
                    pygame.draw.rect(WINDOW, (64,64,64), pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12))
                else:
                    pygame.draw.rect(WINDOW, (32, 32, 32), pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12))
    pygame.display.update()
    WINDOW.fill((255, 255, 255))
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
            elif event.key==pygame.K_g:
                if gui==True:
                    gui=False
                else:
                    gui=True
            elif event.key==pygame.K_c:
                drawCircles+=1
                drawCircles=drawCircles%3
        if event.type==pygame.MOUSEBUTTONDOWN:
            lastPos = pygame.mouse.get_pos()
            if event.button==1 and pygame.Rect(WINDOWdimensions[0]*7/8,0,WINDOWdimensions[0]/8,WINDOWdimensions[1]/12).collidepoint(*pygame.mouse.get_pos()):
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
                    vec = sorted(vec, key=lambda x: abs(x[1]), reverse=True)
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
                    vec = sorted(vec, key=lambda x: abs(x[1]), reverse=True)
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
                    vec = sorted(vec, key=lambda x: abs(x[1]), reverse=True)
                    positions=[]
                    t=0
                    startTime = time.time()
            #print(event.button)
            if event.button==1 and pygame.Rect(0,WINDOWdimensions[1]*11/12,WINDOWdimensions[1]/12,WINDOWdimensions[1]/12).collidepoint(*pygame.mouse.get_pos()):
                drawSurf.fill((255,255,255))
                drawPath=[]
                drawPathComplex=[]
        if event.type == pygame.DROPFILE:
            if drawing==True:
                if os.path.splitext(event.file)[1] in availExt:
                    print('valid image')
                    drawSurf.fill((255,255,255))
                    drawPath=loadImg(event.file)
                else:
                    print('invalid image')