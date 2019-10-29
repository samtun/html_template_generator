# HTML Template Generator

## What is this
This is a simple generator for html templates. It uses Python3 to generate a basic index.html with css and js files. The generator also takes in a favicon. This icon is automatically resized to fit all devices and the needed meta tags are genrated in the html head section.

## Usage
Call ```python3 html_template_generator.py -t <site_title>```

## Arguments
| Argument                           | Description                                                    | Default Value | Required |
|------------------------------------|----------------------------------------------------------------|---------------|----------|
| ```-t```<br>```--title```          | The title of the site                                          | -             | YES      |
| ```-i```<br>```--icon```           | The favicon source file<br>use a 512x512 px file               | favicon.png   | NO       |
| ```-c```<br>```--tileColor```      | Color in the Windows start-menu tile<br>Do NOT include ```#``` | 000000        | NO       |
| ```-j```<br>```--usejQuery```      | Set to True if you want to include jQuery                      | False         | NO       |
| ```--jQueryVersion```              | Set the version of jQuery you'd like to use                    | 3.4.1         | NO       |

## Output
You will find all generated files in the ```output/``` folder.