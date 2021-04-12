"""  this module is for returning the hsv value range of the object selected by user
     use the image from the saved images and then after the detection delete the image
"""

     
        
class ColourFinder:
    def __init__(self):
        #list of images
        self.img=[]
        self.HSV_min=[0,0,0]
        self.HSV_max=[255,255,255]
    
    #function to get the saved images
    def getImages():
        pass
    #function to get the max and min of the HSV from the list of images
    def HSVRange(self):
        
        return self.HSV_min, self.HSV_max
    
        try:
            self.getImages()
        except:
            print("Error: Unable to get the list of saved images\n")
        
        try:
            for images in self.img:
                pass
            
            return self.HSV_min, self.HSV_max
        
        except:
            print("Error: Unable to get the HSV Range of the images\n")
            
