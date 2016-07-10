JS App:

   - Work has ceased here

   - Move to simple Python CGI app for rapid prototyping

   - [dev-]stemsible.crowfly.net

   - See apache config: config/apache/stemsible.conf

   - Landing Page:
       web/index.html  (Single HTML Page App)
       web/js/apps.js  (AngularJS App)

API Server:

   - API Server set up to service JS App (II)

   - Work has ceased here

   - [dev-]stemsible.crowfly.net/api

   - See apache config: config/apache/stemsible.conf

   Example API Calls:

   - stemsible.crowfly.net/api/users
   - stemsible.crowfly.net/api/users/1
   - stemsible.crowfly.net/api/messages
   - stemsible.crowfly.net/api/messages/1

   Back End:
      1. Apache2         (HTTP Server)
      2. web/server.wsgi (WSGI App Server)
      3. lib/server.py   (Python Flask Restful API Server)
      4. lib/users.py    (Python Object Model)
      5. lib/messages.py (Python Object Model)
