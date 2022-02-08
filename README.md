INSTRUCTIONS TO RUN THE PROGRAM
===============================

You need to have Python 3.

You can run the test suite with the following command:
```
python test.py
```

To test the CLI you can enter the project directory and run the `tw.py` script using the following arguments:
- -i <input_file>: <input_file> will be the location of your file with the dice instructions
- -o <output_file>: (optional) can be used to write the result to a file
- -p: tells the program to format the json in a "pretty" way, instead of the compact version


To assure the script has no external dependencies, run using a clear docker image using the command below:
```
docker run -it --rm --name tw-code-challenge -v "$PWD":/usr/src/app -w /usr/src/app python:latest python tw.py -i example_input.txt -p
```