# stemsible

Where Parents talk about their Kid's Education

App:

   - stemsible.crowfly.net

API Server:

   - stemsible.crowfly.net/api

API Call Examples:

   - stemsible.crowfly.net/api/users
   - stemsible.crowfly.net/api/users/1
   - stemsible.crowfly.net/api/messages
   - stemsible.crowfly.net/api/messages/1


High Level Application Architecture

   Front End:

      1. web/index.html  (Single HTML Page App)
      2. web/js/apps.js  (AngularJS App)

   Back End:

      1. Apache2         (HTTP Server)
      2. web/server.wsgi (WSGI App Server)
      3. lib/server.py   (Python Flask Restful API Server)
      4. lib/users.py    (Python Object Model)
      5. lib/messages.py (Python Object Model)
