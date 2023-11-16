The following python libraries are required:

1. Uvicorn
2. fastApi
3. latest version of torchvison

for the front end, i used react.

those are the react dependencies:
1.jest-dom
2.react
3.user-event
4.axios
5.bootstrap
6.canvas
7.mdb-react-ui-kit
8.npm
9.react-bootstrap
10.react-router-dom
11.react-scripts
12.styled-components
13.web-vitals


To test the app, install the required libraries and then open the Main directory "Capstone"

inside Capstone open the Cmd And run :

" py -m uvicorn server:app --reload "

The command will setup a local python server using FastApi.


Then Open a seperate Cmd window in the same directory and enter :
"  cd reactapp"

followed by 

"npm start"

the command will open a react app in your browser at localhost:3000


this will lead you to the main page of the application and from there, you can upload any human/dog image to check for breeds!



