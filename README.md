[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Room-Monitor
The following code demonstrates the intelligent sensors inside Cisco video devices to detect if a meeting room has been left in a state that is not desirable (coffee cups left, missing chairs, whiteboards with corporate sensitive information). It is made up of two scripts;
* Cisco video device macro - detects when there is no one in the room. Then based on the following response, it will post a message into a Webex space (alternatively, it could easily post a message into Service Now or any number of platforms.
* Python script - obtains a picture of the room then sends it to an object detection platform (in this case, Google Vision API). After which returns what objects it detects.

