Was trying to write a HTTP proxy and host it on Heroku for GFW escape.

Failed!!

Heroku uses "Host" header in HTTP to route request to app, which doesn't really
fit the HTTP proxy protocol :(

http_proxy="xxxxx.herokuapp.com:80" curl http://www.google.com would just not
connecting to google.com via the heroku app :(

BTW, tried to use Flask to do so but Flask built-in URL router requires a
leading '/' which is not suitable for HTTP proxy.
