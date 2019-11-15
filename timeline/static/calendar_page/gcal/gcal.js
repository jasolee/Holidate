// date variables
var now = new Date();
today = now.toISOString();

var twoHoursLater = new Date(now.getTime() + (2 * 1000 * 60 * 60));
twoHoursLater = twoHoursLater.toISOString();

// Google api console clientID and apiKey 
var clientId = '252751734600-sedfsdf3286n886jj7gc5m2ugaai.apps.googleufgrcontent.com';
var apiKey = 'AIzsdg5CDEX3PvFyhfghOpnVf4eW_LmfeR80';

// enter the scope of current project (this API must be turned on in the Google console)
var scopes = 'https://www.googleapis.com/auth/calendar';

// OAuth2 functions
function handleClientLoad() {
    gapi.client.setApiKey(apiKey);
    window.setTimeout(checkAuth, 1);
}

function checkAuth() {
    gapi.auth.authorize({ client_id: clientId, scope: scopes, immediate: true }, handleAuthResult);
}

// show/hide the 'authorize' button, depending on application state
function handleAuthResult(authResult) {
    var authorizeButton = document.getElementById('authorize-button');
    var eventButton = document.getElementById('btnCreateEvents');
    var resultPanel = document.getElementById('result-panel');
    var resultTitle = document.getElementById('result-title');

    if (authResult && !authResult.error) {
        authorizeButton.style.visibility = 'hidden';        // if authorized, hide button
        resultPanel.className = resultPanel.className.replace(/(?:^|\s)panel-danger(?!\S)/g, '')    // remove red class
        resultPanel.className += ' panel-success';          // add green class
        resultTitle.innerHTML = 'Application Authorized'        // display 'authorized' text
        eventButton.style.visibility = 'visible';
        $("#txtEventDetails").attr("visibility", "visible");
    } else {                                                    // otherwise, show button
        authorizeButton.style.visibility = 'visible';
        $("#txtEventDetails").attr("visibility", "hidden");
        eventButton.style.visibility = 'hidden';
        resultPanel.className += ' panel-danger';           // make panel red
        authorizeButton.onclick = handleAuthClick;          // setup function to handle button click
    }
}

// function triggered when user authorizes app
function handleAuthClick(event) {
    gapi.auth.authorize({ client_id: clientId, scope: scopes, immediate: false }, handleAuthResult);
    return false;
}

function refreshICalendarframe() {
    var iframe = document.getElementById('divifm')
    iframe.innerHTML = iframe.innerHTML;
}
// setup event details

// function load the calendar api and make the api call
function makeApiCall() {
    var eventResponse = document.getElementById('event-response');
   
    gapi.client.load('calendar', 'v3', function () {                    // load the calendar api (version 3)
        var request = gapi.client.calendar.events.insert
        ({
            'calendarId': '24tn4fht2tr6m86efddfgdfdk@group.calendar.google.com', // calendar ID
            "resource": resource                            // pass event details with api call
        });
        
        // handle the response from our api call
        request.execute(function (resp) {
            if (resp.status == 'confirmed') {
                eventResponse.innerHTML = "Event created successfully. View it <a href='" + resp.htmlLink + "'>online here</a>.";
                eventResponse.className += ' panel-success';
                refreshICalendarframe();
            } else {
                document.getElementById('event-response').innerHTML = "There was a problem. Reload page and try again.";
                eventResponse.className += ' panel-danger';
            }
        });
    });
}
var resource = {
    "summary": "My Event",
    "start": {
        "dateTime": today
    },
    "end": {
        "dateTime": twoHoursLater
    },
    "description":"We are organizing events",
    "location":"US",
    "attendees":[
    {
            "email":"xyz@gmail.com",
            "displayName":"Shaveta",
            "organizer":true,
            "self":false,
            "resource":false,
            "optional":false,
            "responseStatus":"needsAction",
            "comment":"This is event first",
            "additionalGuests":3
            
    },
    {   
        "email":"abc@gmail.com",
            "displayName":"Chatak",
            "organizer":true,
            "self":false,
            "resource":false,
            "optional":false,
            "responseStatus":"needsAction",
            "comment":"This is office event",
            "additionalGuests":3
    }
    ],
};

// FUNCTION TO DELETE EVENT
function deleteEvent() {
 gapi.client.load('calendar', 'v3', function() {  
   var request = gapi.client.calendar.events.delete({
     'calendarId': '24tn4fht2tr6mdfsdfertlsedk@group.calendar.google.com',
     'eventId': 'Hdusrtsbs8'
   });
 request.execute(function(resp) {
    if (resp.status == 'confirmed') {
        alert("Event was successfully removed from the calendar!");
    }
    else{
        alert('An error occurred, please try again later.')
    }
 });
 });
}