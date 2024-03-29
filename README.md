[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Room Monitoring Macro

* [Introduction](https://github.com/dhenwood/Room-Monitor#introduction)
* [Video](https://github.com/dhenwood/Room-Monitor#video)
* [Background](https://github.com/dhenwood/Room-Monitor#background)
* [Setup](https://github.com/dhenwood/Room-Monitor#setup)

## Introduction
The following code demonstrates the intelligent sensors inside Cisco video devices to detect if a meeting room has been left in a state that is not desirable (coffee cups left, missing chairs, whiteboards with corporate sensitive information). 

## Video
A short video of this in action can be found on [Vidcast](https://app.vidcast.io/share/bd8feafe-01b9-43ca-b26f-e1e37a35b6b3)

## Background
It is made up of two scripts; a macro running on the video device and a python script. Whilst I originally had hoped to run all of this from a single macro; there were some limitations that prevented this - notably, the video device has a limit in the body of any POST message (and the size of the image exceeded this). _Note: the method used to obtain the snapshot is not using a publicliy released API._

* [Macro](https://github.com/dhenwood/Room-Monitor/blob/main/RoomMonitor.js) - runs on the video device
* [Python script](https://github.com/dhenwood/Room-Monitor/blob/main/main.py) - runs on a web server. <i>NOTE; this needs direct access to the video device, so cannot be placed on a public web server if the device is inside a corporate network</i>

The following diagram illistrates the interactions of these two scripts, along with querying an image detection engine and posting the output to a Webex space.
![alt text](https://github.com/dhenwood/Room-Monitor/blob/main/FlowDiagram.png?raw=true)

1. The macro running on the video device sends a POST message containing the username and password of the device.
2. Using the username and password (from 1), the Python script requests a specific cookie from the device. The device returns this in a header.
3. Using the cookie, the Python script requests the image (base64 encoded).
4. The Python script sends the image to an object detection engine (in this case Google Vision), where it processess it and returns a JSON response with all objects it has detected.
5. The Python script returns (from step 1) to the video device a summary of items to the video device.
6. The macro assesses what is the expected number of chairs, etc and if it does not equal what the device is configured for, it posts it to a Webex Space.

## Setup
The **Remote Monitoring** license key is **required** to be installed on the endpoint. The Remote Monitoring feature allows an administrator to monitor a room from the endpoint's web interface by getting snapshots from the camera sources connected to the endpoint. To purchase this license, the top level part code required is "**L-TP-RM**", after which you select the appropriate item for the respective device it will run on.

As mentioned above, the Python script needs to run on a server that has direct access to the Cisco video device. It needs to be able to initiate HTTP POST/GET requests to the device.

Once the Macro is installed on the Cisco video device, lines 3, 4, 5 and 6 will need to be updated to reflect the local username and password for the device along with the Webex Bearer token and Space ID.

For the Python script, you will need to create an account on Google Vision. Once done, you will be able to obtain a token and update line 40 to include the key. Alternate object detection services or Python libraries could equally be used instead.
