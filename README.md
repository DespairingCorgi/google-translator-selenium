requirements:
1. glob
2. os
3. time
4. selenium
5. webdriver-manager

How to use:
1. Select file path using FILEPATH variable (the file must be line seperated text file)
2. Select source and target language code
3. run the code

Result:
1. Result file will be created at same directory of the input file
2. naming convention - original_filename_sourcecode-targetcode.txt

Warning:
1. Seldomly, the result would be redundant. This particular result happens due to DELAY system increase delay. (or if this result happens too often, just tell me. I can just write better code for that.)
2. You must install library requirements.
3. Do not run this code parallely. (You can, but not recommended)

Tips:
1. The FILEPATH variable can be both absolute/relative path.
2. If the browser instantly closes, the driver increase DELAY variable.

If you have any other quetions, please contact me.
