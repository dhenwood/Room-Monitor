import xapi from 'xapi';

const username = "<removed>" // local device user account
const password = "<removed>" // password for local device user account
const webexToken = "<removed>" // for posting to a Webex Space
const webexSpaceId = "<removed>" // for posting to a Webex Space
const correctChairs = 4 // Adjust this number to the appropriate value for the room
const correctTables = 1 // Adjust this number to the appropriate value for the room

// Get Device Name (to identify it when posting into Webex Space)
var deviceName;
xapi.status.get('SystemUnit BroadcastName').then ((value) => {
  deviceName = value
})


function queryServer(){
  const url = "http://anzbots.cisco.com:5000?username=" + username + "&password=" + password
  xapi.command('HttpClient Get', { 'Url':url, 'AllowInsecureHTTPS': 'True'}).then(
    (result) => {
    var body = result.Body;
    console.log("myResponse: " + body)

    var bodyJson = JSON.parse(body)
    var chairCount = bodyJson.chairs
    var tableCount = bodyJson.tables
    
    if(chairCount != correctChairs){
      console.log("ALERT: Incorrect chairs. We see " + chairCount + " when there should be " + correctChairs)
      const message = deviceName + " has the incorrect number of chairs. I counted " + chairCount + " when there should be " + correctChairs
      postAlertToSpace(message)
    }

    if(tableCount != correctTables){
      console.log("ALERT: Incorrect tables. We see " + tableCount + " when there should be " + correctTables)
      const message = deviceName + " has the incorrect number of tables. I counted " + tableCount + " when there should be " + correctTables
      postAlertToSpace(message)
    }
  });
}

function postAlertToSpace(message){
  const url = 'https://webexapis.com/v1/messages';
  const contentType = "Content-Type: application/json";
  const bearerToken = "Authorization: Bearer " + webexToken;

  var body = {
    'roomId' : webexSpaceId,
    'text' : message
  };

  xapi.command('HttpClient Post', { 'Header': [contentType, bearerToken] , 'Url':url, 'AllowInsecureHTTPS': 'True'}, JSON.stringify(body));
}


console.log('Adding feedback listener to: RoomAnalytics PeopleCount');
xapi.status.on('RoomAnalytics PeopleCount', (count) => {
  if (count.Current) {
    console.log(`Updated current count: ` + count.Current);
    if (count.Current == 0){
      console.log("no one in the room...checking room")
      queryServer()
    }
  }
})
