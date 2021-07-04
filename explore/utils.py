# -*- coding: utf-8 -*-

def arabic_slugify(string):
    """
    Slugify a given string. 
    """
    string = string.replace(" ", "-")
    string = string.replace(",", "-")
    string = string.replace("(", "-")
    string = string.replace(")", "")
    string = string.replace("؟", "")
    string = string.replace("!", "")
    return string