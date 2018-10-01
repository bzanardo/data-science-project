/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow
 */

var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
var cors = require('cors');
var querystring = require('querystring');
var cookieParser = require('cookie-parser');

var client_id = 'ba55c7d3a7df4cfeb32d17775fa6ceca'; // Your client id
var client_secret = 'fb85f14c92c948449c0b943742fc7b78'; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri

const fs = require('fs');

/**
 * Generates a random string containing numbers and letters
 * @param  {number} length The length of the string
 * @return {string} The generated string
 */
var generateRandomString = function(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

var stateKey = 'spotify_auth_state';

var app = express();

app.use(express.static(__dirname + '/public'))
   .use(cors())
   .use(cookieParser());

app.get('/login', function(req, res) {

  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // your application requests authorization
  var scope = 'user-read-private user-read-email';
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});

app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        var access_token = body.access_token,
            refresh_token = body.refresh_token;


        var options = {
          url: 'https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        };

        var tracks = [];
        var ids = "";
        var audio_features = [];

        // use the access token to access the Spotify Web API
        request.get(options, function(error, response, body) {
        	
        	for (var i = 0; i < body["items"].length; i++) {
        		tracks.push({
        			id:  body["items"][i]["track"]["id"] , 
        			values: {
        				name: body["items"][i]["track"]["name"], 
        				artists: body["items"][i]["track"]["artists"], 
        				popularity: body["items"][i]["track"]["popularity"]
        			}
        		});
        		//ids.push(body["items"][i]["track"]["id"]);
        		ids = ids + String(body["items"][i]["track"]["id"]) + ",";
        	}
        

        //fs.writeFileSync('top50.json', JSON.stringify(tracks)); 

		ids = ids.substring(0, ids.length - 1);

    	var URL = 'https://api.spotify.com/v1/audio-features/?ids=' + ids;
    	var options = {
      		url: URL,
      		headers: { 'Authorization': 'Bearer ' + access_token },
      		json: true
    	}

        request.get(options, function(error, response, body) {
        		for (var i = 0; i < body["audio_features"].length; i++) {
        			for (var key in tracks) {
        				if (body["audio_features"][i]["id"] == tracks[key]["id"]) {
        					for (var k in body["audio_features"][i]){
        						tracks[key]["values"][k] = body["audio_features"][i][k];
        					}
        				}
        			}
        			/*audio_features.push({
        				id: body["audio_features"][i]["id"] , 
        				values: body["audio_features"][i]
        				
        			});*/
        		}
        	
        	fs.writeFileSync('top50.json', JSON.stringify(tracks)); 	
        });

        var randomQuery = generateRandomString(1);
        var randomOffset = (Math.floor(Math.random() * 1000));

        var options = {
      		url: 'https://api.spotify.com/v1/search?q=' + randomQuery + '&type=track&market=US&limit=50&offset=' + String(randomOffset),
      		headers: { 'Authorization': 'Bearer ' + access_token },
      		json: true
    	}

    	var randomTracks = [];
    	var randomIds = "";

        request.get(options, function(error, response, body) {
        		for (var i = 0; i < body["tracks"]["items"].length; i++) {
	        		randomTracks.push({
	        			id:  body["tracks"]["items"][i]["id"] , 
	        			values: {
	        				name: body["tracks"]["items"][i]["name"], 
	        				artists: body["tracks"]["items"][i]["artists"], 
	        				popularity: body["tracks"]["items"][i]["popularity"]
	        			}
	        		});
	        		//ids.push(body["items"][i]["track"]["id"]);
	        		randomIds = randomIds + String(body["tracks"]["items"][i]["id"]) + ",";
        		}

        randomIds = randomIds.substring(0, randomIds.length - 1);

    	var URL = 'https://api.spotify.com/v1/audio-features/?ids=' + randomIds;
    	var options = {
      		url: URL,
      		headers: { 'Authorization': 'Bearer ' + access_token },
      		json: true
    	}
    	console.log(URL)

        request.get(options, function(error, response, body) {
        		for (var i = 0; i < body["audio_features"].length; i++) {
        			for (var key in randomTracks) {
        				if (body["audio_features"][i]["id"] == randomTracks[key]["id"]) {
        					for (var k in body["audio_features"][i]){
        						randomTracks[key]["values"][k] = body["audio_features"][i][k];
        						console.log(body["audio_features"][i][k]);
        					}
        				}
        			}
        			/*audio_features.push({
        				id: body["audio_features"][i]["id"] , 
        				values: body["audio_features"][i]
        				
        			});*/
        		}

        	console.log(randomTracks)
        	
        	fs.writeFileSync('random1.json', JSON.stringify(randomTracks)); 
        	});	
        });

        });


        // we can also pass the token to the browser to make requests from there
        res.redirect('/#' +
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }));
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
});

app.get('/refresh_token', function(req, res) {

  // requesting access token from refresh token
  var refresh_token = req.query.refresh_token;
  var authOptions = {
    url: 'https://accounts.spotify.com/api/audio-features',
    headers: { 'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64')) },
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token;
      res.send({
        'access_token': access_token
      });
    }
  });
});

console.log('Listening on 8888');
app.listen(8888);
