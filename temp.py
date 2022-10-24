import numpy as np
import cv2 as cv2
import matplotlib.pylab as plt
def segColorKMeans(imagen,K):
    
    twoDimage = imagen.reshape((-1,1))
    twoDimage = np.float32(twoDimage)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    attempts=10

    ret,label,center=cv2.kmeans(twoDimage,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((imagen.shape)) , ret , label,  center
    


def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)


imagen = cv2.imread('F4.jpeg')
#cv2.imshow('IMAGEN ORIGINAL',cv2.resize(imagen,(680,500))) 

imGray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#cv2.imshow('IMAGEN ESCALA DE GRIS',cv2.resize(imGray,(680,500))) 



imagen_fil = cv2.medianBlur(imGray, 7)
#cv2.imshow('Filtro ',cv2.resize(imagen_fil,(680,500))) 



# Blur the image
imagen_gauss = cv2.GaussianBlur(imagen_fil, (3,3), 0)

# Apply Unsharp masking
imagen_highboost = cv2.addWeighted(imagen_fil, 2, imagen_gauss, -1, 0)
#cv2.imshow('Filtro highboost',cv2.resize(imagen_highboost,(680,500)))


imagen_gama = adjust_gamma(imagen_highboost,0.95)
cv2.imshow('Correcion gama',cv2.resize(imagen_gama,(680,500)))




plt.hist(imGray.ravel(),bins = 256, range = [0, 256])
plt.title("Gris")
plt.show()

plt.hist(imagen_fil.ravel(),bins = 256, range = [0, 256])
plt.title("Filtro mediana")
plt.show()

plt.hist(imagen_gama.ravel(),bins = 256, range = [0, 256])
plt.title("Correcion gama")
plt.show()


plt.hist(imagen_highboost.ravel(),bins = 256, range = [0, 256])
plt.title("Highboost")
plt.show()






#cv2.imshow('Klosterizaciòn sin filtro',segColorKMeans(imagen,5))
imagen_KMeans ,ret , label,  center  =  segColorKMeans(cv2.resize(imagen_gama,(680,500)),4)
#cv2.imshow('clustering',imagen_KMeans)

print(sum(label))
label = np.uint8(label)
grupo =  label.reshape((imagen_KMeans.shape))

grupo1 = np.where(grupo == 1, 1 , 0)
grupo2 = np.where(grupo == 2, 1 , 0)
grupo1 = np.uint8(1 - grupo1) 

dist = cv2.distanceTransform(grupo1, cv2.DIST_L2, 3)
cv2.imshow('Grupo 1', grupo1*255)


cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
cv2.imshow('Distance Transform Image', dist * grupo2)



'''
methods = [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED]


for method in methods:
    {res = cv2.matchTemplate(image_gray, template_gray, method=method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)
    
    if method == cv2.TM_SQDIFF or method == cv2.TM_SQDIFF_NORMED:
    x1, y1 = min_loc
    x2, y2 = min_loc[0] + template.shape[1], min_loc[1] + template.shape[0]
    else:
    x1, y1 = max_loc
    x2, y2 = max_loc[0] + template.shape[1], max_loc[1] + template.shape[0]
    
    cv2.rectangle(Copia, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.imshow("Image", Copia)
    cv2.imshow("Template", Muestra)
    Copia = imagen.copy()}
'''       
        
'''
points = np.array([(0,240),(320,240),(226,100),(94,100)], dtype = np.int32)
ROI = np.zeros_like(imGray)
ignore_mask_color = 255
cv2.fillPoly(ROI, points, ignore_mask_color)
masked_image = cv2.bitwise_and(imGray, ROI)
cv2.imshow('IMAGEN ESCALA DE GRIS',cv2.resize(imGray,(680,500))) 
'''

'''
#normalizada = cv2.normalize(imGray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
#for i in range(0,4):
#  normalizada = (3*normalizada**2-2*normalizada**3)
#im3 = normalizada*255
cv2.imshow('Imagen normalizada',np.concatenate((cv2.resize(imGray,(450,300)), cv2.resize(im3,(450,300))), axis=1))

alpha = 1.2 # Constraste (1.0-3.0)
beta = 15 # Brillo (0-100)

adjusted = cv2.convertScaleAbs(imGray, alpha=alpha, beta=beta)
cv2.imshow('IMAGEN CON NUEVO BRILLO',cv2.resize(adjusted,(680,500))) 
'''

'''
gaussiana = cv2.GaussianBlur(imGray, (7,7), 0)
unsharp_image = cv2.addWeighted(imGray, 2, gaussiana, -1, 0)


cv2.imshow('IMAGEN CON FILTRO GAUSSIANO',cv2.resize(gaussiana,(680,500))) 
cv2.imshow('IMAGEN CON BORDES ',cv2.resize(unsharp_image,(680,500))) 


'''

'''
apertureSize  = 3
edge = cv2.Canny(gaussiana, 50, 150,apertureSize=5)
cv2.imshow('BORDES',cv2.resize(edge,(680,500))) 
'''




cv2.waitKey(0)
cv2.destroyAllWindows(1)



