<font size= 5>Hello Vero Digital Solutions Team! </font>
<p>
<font size = 3>
In this instruction, I will list all of the commands required to run this script.

<font size = 4>Before running the server and client you need to install a few python packages:</font>
<p><strong>Argparse</strong>: This package is used to parse command-line arguments.</p>
<p><strong>Openpyxl</strong>: This package is used to create and modify Excel files.</p>
<p><strong>Requests</strong>: This package is used to send HTTP requests.</p>
<p><strong>Uvicorn</strong>: This package is used to start the server.</p>
<p><strong>FastAPI</strong>: This package is used as web framework.</p>

To install these packages, you can use the following command:
<strong>
<p>pip install uvicorn</p>
<p>pip install argparse</p>
<p>pip install openpyxl</p>
<p>pip install requests</p>
<p>pip install fastapi</p>
</strong>

<font size=4>Please enter the following command to run the <strong>server</strong>.</font>

<font size =3> <strong> uvicorn server:app --reload </strong></font>

Authorization is done automatically by the auth.py module by updating the access token at each start

To run the <strong>client</strong> script the following command is needed:

<font size = 3> <strong>python client.py -k gruppe hu info </strong> </font>

You can also use the --help option to display the full list of available options:

<font size = 3> <strong> python client.py --help </strong> </font>
</font>
</p>