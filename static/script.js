const video = document.getElementById("video");
const photo = document.getElementById("photo");

let stream;

// Start Camera
async function startCamera(){

    try{

        stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        video.srcObject = stream;

        video.style.display = "block";
        photo.style.display = "none";

    }

    catch(error){

        console.log(error);

        alert(error.message);
    }
}

// Capture Image
function captureImage(){

    const canvas = document.getElementById("canvas");

    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0);

    // Convert image
    const image = canvas.toDataURL("image/png");

    // Show image in same box
    photo.src = image;

    photo.style.display = "block";

    video.style.display = "none";

    // Stop camera
    stream.getTracks().forEach(track => track.stop());
}