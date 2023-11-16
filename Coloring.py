import random

class Coloring:
    @staticmethod
    def getRandomColorValue():
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        return Coloring.rgb_to_hex((r,g,b))
    
    @staticmethod
    def rgb_to_hex(rgb):
        # Ensure RGB values are within the valid range (0-255)
        r, g, b = [max(0, min(255, int(x))) for x in rgb]
        
        # Convert to HEX format
        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        
        return hex_color
    
    @staticmethod
    def normalizeToColors(min,max,actualValue):
        factor = (actualValue - min) / (max - min)
        red   = int(255*factor)
        green = int(255*(1-factor))
        blue  = 0
        rgb = (red,green,blue)
        
        return Coloring.rgb_to_hex(rgb)