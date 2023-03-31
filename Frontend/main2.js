
function search()
{
	var searchBox = document.getElementsByClassName('searchbar')[0];
	console.log(searchBox.value);

	if (!searchBox.value)
	{
		alert('Please enter a valid text');
	}
	else
	{
		getPhotos(searchBox.value.trim().toLowerCase());
	}
}

function getPhotos(text)
{
	var photosDiv = document.getElementById('photos_results');
	photosDiv.innerHTML = "";

	document.getElementsByClassName('searchbar')[0].value = '';

 	var sdk = apigClientFactory.newClient({ apiKey: "mcMOdJHYUg8yvAjRZ9aLH2YPKg7WJUDG4qTDFvEV" });

    sdk.searchGet({ q: text, "x-api-key": "mcMOdJHYUg8yvAjRZ9aLH2YPKg7WJUDG4qTDFvEV"})
    	.then(function(result) {
    		console.log(result['data']['message']);
				console.log(result);
    		var photo_results = result['data']['message'];

            if (photo_results.length == 0)
            {
                alert("No images found for your search");
            }

    		var photosDiv = document.getElementById('photos_results');
    		photosDiv.innerHTML = "";
				fetch()
    		for (var i=0; i<photo_results.length; i++)
    		{
    			console.log(photo_results[i]);
    			photosDiv.innerHTML += "<figure><img src=" + photo_results[i] + " style='width:45%'></figure>"
    		}
    	}).catch(function(result){
    		console.log(result);
    	});
}

function uploadRequest(body, file, custom_labels)
{
	url = "https://92wrywms2h.execute-api.us-east-1.amazonaws.com/v1/upload/photos-bucket-vwks/" + file.name;
	console.log(file);
	if(custom_labels.length >0)
	{
		console.log("possible custom label")
		const response = fetch(url, {
			method: 'PUT',
			headers: {
				'Content-Type': file.type,
				"x-api-key": "mcMOdJHYUg8yvAjRZ9aLH2YPKg7WJUDG4qTDFvEV",
				"X-amz-meta-customLabels":custom_labels
			},
			body: JSON.stringify(body)
		});
	}
	else{
		console.log("no custom label")
		const response = fetch(url, {
			method: 'PUT',
			headers: {
				'Content-Type': file.type,
				"x-api-key": "mcMOdJHYUg8yvAjRZ9aLH2YPKg7WJUDG4qTDFvEV"
			},
			body: JSON.stringify(body)
		});
	}
}

function upload()
{
	var filePath = (document.getElementById('uploaded_file').value).split("\\");
	const uploadedFile = document.getElementById('uploaded_file').files[0];
	console.log(uploadedFile);
	custom_labels = ""
	if (!document.getElementById('custom_labels').value == "") {
			var custom_labels = document.getElementById('custom_labels').value;
	}
	const formData = new FormData();
	formData.append('file',uploadedFile);
	formData.append('labels',custom_labels);

	const fileInput = document.getElementById('uploaded_file');
	const fileName = fileInput.value.split('\\').pop();
	const fileType = fileName.split('.').pop();

	url = "https://92wrywms2h.execute-api.us-east-1.amazonaws.com/v1/upload/photos-bucket-vwks/" + fileName;

	if(custom_labels.length >0)
	{
		console.log("possible custom label")
		const response = fetch(url, {
			method: 'PUT',
			headers: {
				'Content-Type': `image/${fileType}`,
				"x-api-key": "mcMOdJHYUg8yvAjRZ9aLH2YPKg7WJUDG4qTDFvEV",
				"X-amz-meta-customLabels":custom_labels
			},
			body: uploadedFile
		});
	}
	else{
		console.log("no custom label")
		const response = fetch(url, {
			method: 'PUT',
			headers: {
				'Content-Type': file.type,
				"x-api-key": "mcMOdJHYUg8yvAjRZ9aLH2YPKg7WJUDG4qTDFvEV"
			},
			body: uploadedFile
		});
	}

}

window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition

function interpretVoice()
{
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }

    var searchBox = document.getElementsByClassName('searchbar')[0];
    const recognition = new window.SpeechRecognition();

    mic = document.getElementById("switch");

    if (mic.innerHTML == "micOn") {
        recognition.start();
    } else if (mic.innerHTML == "micOff"){
        recognition.stop();
    }


    recognition.addEventListener("start", function() {
        console.log("reached")

        mic.innerHTML = "micOff";
        console.log("Recording.....");
    });

    recognition.addEventListener("end", function() {
        console.log("Stopping recording.");
        mic.innerHTML = "micOn";
    });

    recognition.addEventListener("result", resultOfSpeechRecognition);
    function resultOfSpeechRecognition(event) {
        const current = event.resultIndex;
        transcript = event.results[current][0].transcript;
        searchBox.value = transcript;
        console.log("transcript : ", transcript)
    }
}
