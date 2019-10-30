# html template generator
# input a 512x512 px file and a site name to start

from PIL import Image
from bs4 import BeautifulSoup, Tag
from enum import Enum
import sys, getopt
import urllib.request
import json

def main(argv):
    class SizeType(Enum):
        DEFAULT = 1
        APPLE = 2
        WINDOWS = 3

    # title of the site
    title = None 
    # iconFile to use as favicon
    iconFile = "favicon.png"
    # tile color for windows start menu 
    tileColor = "#000000"
    # the jQuery version to use
    jQueryVersion = "3.4.1"
    # toggle jQuery usage
    usejQuery = False

    # get arguments from call
    opts, args = getopt.getopt(argv, 
        "t:i:c:j:", 
        ["icon=", "title=", "tileColor=", "jQuery="])

    for opt, arg in opts:
        if opt in ("-t", "--title"):
            title = arg
        elif opt in ("-i", "--icon"):
            iconFile = arg
        elif opt in ("-c", "--tileColor"):
            tileColor = arg
        elif opt in ("-j", "--jQuery"):
            usejQuery = arg

    if title == None:
        print("Please provide a title via -t or --title")
        sys.exit()
    # if unasigned use default value
    if iconFile == None:
        iconFile = "favicon.png"

    # load icon
    iconFile = "favicon.png" 
    ext = iconFile[iconFile.rfind('.'):]
    favicon = Image.open(iconFile)
    outputDir = "output/"
    print("-- Generating icons and index.html")

    # icon sizes
    sizes = {
        512: [SizeType.DEFAULT],
        384: [SizeType.DEFAULT],
        256: [SizeType.DEFAULT],
        192: [SizeType.DEFAULT],
        180: [SizeType.APPLE],
        167: [SizeType.APPLE],
        152: [SizeType.APPLE],
        144: [SizeType.DEFAULT, SizeType.WINDOWS],
        120: [SizeType.APPLE],
        114: [SizeType.APPLE],
        96: [SizeType.DEFAULT],
        76: [SizeType.APPLE],
        72: [SizeType.APPLE],
        60: [SizeType.APPLE],
        57: [SizeType.APPLE],
        48: [SizeType.DEFAULT]
    }

    # generate index.html and favicons
    with open("stubs/index.html") as inf:
        txt = inf.read()
        soup = BeautifulSoup(txt, features="html.parser")

    # insert icons, tileColor and manifest in the head section
    soup.title.string = title
    for size, types in sizes.items():
        for type in types:
            sizeString = str(size)
            favicon.resize((size,size), Image.ANTIALIAS).save(outputDir + "img/favicon/favicon-" + sizeString + "x" + sizeString + ext)
            
            if type != SizeType.WINDOWS:
                soup.head.append(
                    soup.new_tag(
                        "link", 
                        rel = "icon" if type == SizeType.DEFAULT else "apple-touch-icon", 
                        type = "image/png", 
                        size = sizeString + "x" + sizeString,
                        href = "img/favicon/favicon-" + sizeString + "x" + sizeString + ext))
            else:
                soup.head.append(Tag(
                    builder = soup.builder, 
                    name = "meta", 
                    attrs = {
                        "name": "msapplication-TileImage",
                        "content": "img/favicon/favicon-" + sizeString + "x" + sizeString + ext, 
                    }))

    soup.head.append(Tag(
        builder = soup.builder, 
        name = "meta", 
        attrs = {
            "name": "msapplication-TileColor",
            "content": "#" + tileColor
        }))

    manifestStub = open('stubs/manifest.json', 'r')
    data = json.load(manifestStub)
    data['name'] = title
    data['short_name'] = title
    data['theme_color'] = tileColor
    data['background_color'] = tileColor
    with open(outputDir + "img/favicon/manifest.json", "w") as outf:
        outf.write(json.dumps(data))

    # add css and javascript
    if (usejQuery):
        jQueryFileName = "jquery-" + jQueryVersion + ".min.js"
        print("-- Including jQuery")
        url = "http://code.jquery.com/" + jQueryFileName
        response = urllib.request.urlopen(url)

        with open(outputDir + "js/" + jQueryFileName, "w") as outf:
            outf.write(response.read().decode('utf-8'))
            soup.head.append(
                soup.new_tag(
                    "script", 
                    src = "js/" + jQueryFileName))
    
    print("-- Generating js and css files")

    cssContent = open("stubs/styles.css", "r").read()
    with open(outputDir + "css/styles.css", "w") as outf:
        outf.write(cssContent)
        soup.head.append(
            soup.new_tag(
                "link", 
                href = "css/styles.css",
                rel = "stylesheet"))

    jsContent = open("stubs/script_jquery.js" if usejQuery else "stubs/script.js", "r").read()
    with open(outputDir + "js/script.js", "w") as outf:
        outf.write(jsContent)
        soup.head.append(
            soup.new_tag(
                "script", 
                src = "js/script.js"))
    
    with open(outputDir + "index.html", "w") as outf:
        outf.write(str(soup.prettify()))

if __name__ == "__main__":
   main(sys.argv[1:])

