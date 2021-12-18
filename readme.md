# drive folder copier

Google drive doesn't allow you to copy folders from your main drive to a team drive/shared drive. This is a hassle when you have to move folders with a lot of smaller sub folders in it. This simple python scripts does that easily for you.

## How to Use
* pip install -r requirements.txt (needs python version > 2.6) ps: seems like the requirements list is fucked up and listed all the global packages, please use your own discretion

* Place your GDrive API credentials or use the included hacky quickstart one

*  This script takes 3 inputs:

        * folderid - The id of the folder whose contents you want to copy over
        * destid - The id of the destination folder
        * driveid - The destination folder's team drive id

    It will copy all the contents of the folder with the given folder id and and paste them in the destination folder.

Note: The last part of the folder url will be its id
        For a folder with url ```https://drive.google.com/drive/folders/0B_Hy5UChYJu0T2JsVFFyTnM1YTg```, its id will be ```0B_Hy5UChYJu0T2JsVFFyTnM1YTg```
