"""CSCI 445 - Case Study #2
"""
def adjust(c):
    return c / 12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def relative_luminance(color):
    """Calculate the relative luminance of a color using the formula:"""
    r,g,b = color 
    r = r/255
    g = g/255
    b = b/255 
    
    r = adjust(r)
    g = adjust(g)
    b = adjust(b)
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast_ratio(forground, background):
    """Compute the contrast ratio between two colors using their relative luminance"""
    lum1 = relative_luminance(forground)
    lum2 = relative_luminance(background)
    
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)

def check_wcag(foreground, background):
    """Ceck if the color combination meets WCAG AA standards for normal text (contrast ratio of at least 4.5:1)"""
    ratio = contrast_ratio(foreground, background)
    if ratio >= 4.5:
        print("PASS: Meets WCAG AA for normal text")
    else:
        print("FAIL: Does not meet WCAG AA for normal text")
        print("Recommendation: Increase contrast ratio to at least 4.5:1")
        
# Example usage:
foreground_color = (180,180,180) # Light gray
background_color = (54,57,63) # Dark gray

print("Checking Discord-like color combination:")
check_wcag(foreground_color, background_color)
    