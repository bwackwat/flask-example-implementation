function post($uritext, $data)
{
	$json = $data | ConvertTo-Json
	$uri = New-Object System.Uri($uritext)

	"POSTING"
	$json
	"TO " + $uritext

	$response = Invoke-WebRequest -Uri $uri -Method POST -Body $json
	$response.content
}

post "http://localhost:5000/signup" @{username='bwackwat',email='john.has.come@gmail.com',password='aq12ws'}

post "http://localhost:5000/signup" apples